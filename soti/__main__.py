"""
The main soti front-end script which initializes the terminal and listener threads.
"""

import multiprocessing
import cmd
import serial.tools.list_ports
import serial.tools.list_ports_common

from utils import help_strings
from utils.constants import (
    NodeID, CmdID, COMM_INFO
)

from serial_reader import serial_reader
from session_logger import log_messages
from message import Message
import parser


# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class CommandLine(cmd.Cmd):
    """Represents the command line interface."""
    # initialize the object
    def __init__(self, out_queue, write_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\niamnow\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_queue
        self.write_msg_queue = write_queue
        self.sender_id = NodeID.CDH


    def do_send(self, arg):
        """Sends a command."""
        try:
            cmd_str, data, options = parser.parse_send(arg)

            # get corresponding CmdID
            try:
                cmd_id = CmdID(parser.parse_int(cmd_str))
            except ValueError:
                raise parser.ArgumentException("Invalid command ID")

            # get the default values for the command
            priority = COMM_INFO[cmd_id]["priority"]
            sender_id = self.sender_id
            dest_id = COMM_INFO[cmd_id]["dest"]

            # override defaults with optional arguments
            for key in options:
                if key == "priority":
                    priority = parser.parse_int(options["priority"])

                try:
                    if key == "from":
                        sender_id = NodeID(parser.parse_int(options["from"]))
                    if key == "to":
                        dest_id = NodeID(parser.parse_int(options["to"]))
                except (ValueError, KeyError):
                    raise parser.ArgumentException("Invalid node ID")

            # raise exceptions for invalid arguments
            if not (0 <= priority <= 32):
                raise parser.ArgumentException("Invalid priority")

            if dest_id is None:
                raise parser.ArgumentException(f"{cmd_id.name} requires a recipient")

            print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

            # create a message using the arguments
            msg = Message(priority, sender_id, dest_id, cmd_id, data, source="user")

            # send the message to be written to the serial device and logged
            self.write_msg_queue.put(msg)
            self.out_msg_queue.put(msg)

        except (ValueError, parser.ArgumentException) as e:
            print(e)
            return


    def do_iamnow(self, arg):
        """Changes the default sender ID."""
        try:
            node_id = NodeID(parser.parse_int(arg))
            if node_id in NodeID:
                self.sender_id = node_id
                print(f"Updated sender ID to {self.sender_id.get_display_name()}.")
            else:
                print("Invalid sender ID.")
        except ValueError:
            print("Invalid args.")


    def do_help(self, arg):
        """Displays help messages."""
        if arg == "send":
            cmd_method = getattr(self, "do_send")
            print(f"Description: {cmd_method.__doc__}")
            print(f"Usage: send <command> [data1 ...] [option=value ...]")
        else:
            print(help_strings.HELP_MESSAGE)


    def do_list(self, _):
        """Lists the available CAN commands."""
        print(help_strings.COMMAND_LIST)


    def do_exit(self, _):
        """Exits the CLI."""
        return True


# ----------------------------------------------------------
# MAIN APPLICATION CODE
# ----------------------------------------------------------

# ascii art lol
# font taken from https://patorjk.com/software/taag/
SPLASH = """
_._*_   ________  __________ .__'_        _
___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____
.___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>
_'._ /___/\\____/ /_/ /___/   *_.__       /_/
"""


if __name__ == "__main__":
    try:
        print(SPLASH)
        print("\nWelcome to the SOTI CLI!\n")

        print("Available Input Sources:")

        virtual_port = serial.tools.list_ports_common.ListPortInfo("Virtual")
        virtual_port.description = "Run in virtual mode for off-board testing."

        sources = sorted(serial.tools.list_ports.comports()) + [virtual_port]

        for i, port in enumerate(sources):
            print(str(i) + ": " + port.device + " - " + port.description)
        print()

        # Prompt user for valid port.
        while True:
            try:
                source_number = int(input("Please choose an input source:"))
                selected_port = sources[source_number]
                break
            except (ValueError, IndexError):
                pass
            print("Invalid input. Please enter the number corresponding to your selection.")

        virtual_mode = selected_port is virtual_port

        multiprocessing.set_start_method('spawn')
        write_msg_queue = multiprocessing.Queue() # messages to be written to file
        out_msg_queue = multiprocessing.Queue() # messages to send to SOTI board

        # thread-safe flags to tell the processes to stop.
        stop_serial_reader_flag = multiprocessing.Event()
        stop_session_logger_flag = multiprocessing.Event()

        processes = []

        # create the serial handler process
        if not virtual_mode:
            processes.append(multiprocessing.Process(
                target=serial_reader,
                args=(
                    write_msg_queue,
                    out_msg_queue,
                    stop_serial_reader_flag,
                    selected_port.device
                    ),
                daemon=True)
            )

        # create the session logger process
        processes.append(multiprocessing.Process(
            target=log_messages,
            args=(
                write_msg_queue,
                stop_session_logger_flag,
                selected_port.device
            ),
            daemon=True)
        )

        # start the processes
        for p in processes:
            p.start()

        CommandLine(out_msg_queue, write_msg_queue).cmdloop()

    except KeyboardInterrupt:
        pass

    finally:
        # tell the processes to stop
        stop_serial_reader_flag.set()
        stop_session_logger_flag.set()

        for p in processes:
            p.join()

        print("\nExiting...")
