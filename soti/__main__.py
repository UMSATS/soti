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


class ArgumentException(Exception): pass

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
            cmd_str, data, options, parse_error = parse_send(arg)
            
            # resolve command argument to corresponding ID
            cmd_id = parse_int(cmd_str)
            if cmd_id is None or cmd_id >= len(CmdID):
                raise ArgumentException("Invalid command code")
            cmd_id = CmdID(cmd_id)

            # get the default values for the command
            priority = COMM_INFO[cmd_id]["priority"]
            sender_id = self.sender_id
            dest_id = COMM_INFO[cmd_id]["dest"]
            
            # override defaults with optional arguments
            for key in options:
                if key == "priority":
                    priority = parse_int(options["priority"])
                
                try:
                    if key == "from":
                        sender_id = NodeID(parse_int(options["from"]))
                    if key == "to":
                        dest_id = NodeID(parse_int(options["to"]))
                except KeyError:
                    raise ArgumentException("Invalid node ID")
            
            # raise exceptions for invalid arguments
            if parse_error:
                raise ArgumentException(parse_error)
            
            if not (0 <= priority <= 32):
                raise ArgumentException("Invalid priority")
            
            if dest_id is None:
                raise ArgumentException(f"{cmd_id.name} requires a recipient")

            # truncate excess data arguments
            data = data[:14]
            
            # pad data with zeros to create a full message
            data = data.ljust(14, "0")

            print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

            # create a message using the arguments
            msg = Message(priority, sender_id, dest_id, cmd_id, bytes.fromhex(data), source="user")

            # send the message to be written to the serial device and logged
            self.write_msg_queue.put(msg)
            self.out_msg_queue.put(msg)

        except (ValueError, ArgumentException) as e:
            print(e)
            return


    def do_iamnow(self, arg):
        """Changes the default sender ID."""
        try:
            node_id = NodeID(parse_int(arg))
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
# FUNCTIONS
# ----------------------------------------------------------

def parse_send(args: str) -> tuple[str, str, dict, str]:
    """Parses arguments for `do_send`."""
    parts = args.split()

    cmd_id = parts[0]
    data = ""
    options = {}
    error = ""

    for index, part in enumerate(parts[1:]):
        try:
            # check if key-value pair
            if '=' in part:  
                key, value = part.split('=')
                options[key] = value

            # else treat as data argument
            else:
                # value is a hex string (ex. "7b")
                value = format(parse_int(part), 'x')

                # add zeros to match nearest int size (8, 16, 32 bits)
                if part[:2] == "0b":
                    # subtract prefix and round up
                    digits = (len(part) - 2 + 3) // 4
                elif part[:2] == "0x":
                    digits = (len(part) - 2)
                else:
                    digits = len(value)
                target_digits = 2
                while target_digits < digits: target_digits *= 2
                value = value.rjust(target_digits, "0")

                # append value to data
                data += value

        except ValueError:
            error = f"Unknown argument '{part}'"
    
    return cmd_id, data, options, error

def parse_int(i) -> int:
    """Casts numbers and enum members to int."""
    try:
        if isinstance(i, int):
            return i
        elif isinstance(i, str):
            if i.isnumeric():
                return int(i)
            if i[:2] == "0x":
                return int(i, 16)
            if i[:2] == "0b":
                return int(i, 2)
            if i in NodeID.__members__:
                return NodeID[i].value
            if i in CmdID.__members__:
                return CmdID[i].value
        else:
            # no valid cast
            raise ValueError()
    except (ValueError) as e:
        # raises an exception for the caller
        raise ValueError(e) from e

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
