"""
The main soti front-end script which initializes the terminal and listener threads.
"""

import multiprocessing
import threading
import cmd
import serial.tools.list_ports
import serial.tools.list_ports_common

from utils import help_strings
from utils.constants import CmdID, NodeID

from serial_reader import serial_reader
from session_logger import log_messages, dict_to_yaml
import parser

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
import shlex

enable_printing = threading.Event()
enable_printing.set()

do_exit = False

# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

# class CommandLine(cmd.Cmd):
#     """Represents the command line interface."""
#     # initialize the object
#     def __init__(self, out_queue, write_queue):
#         super().__init__()
#         self.intro = "\nAvailable commands:\nsend\niamnow\nhelp\nlist\nexit\n"
#         self.prompt = ">> "
#         self.out_msg_queue = out_queue
#         self.write_msg_queue = write_queue
#         self.sender_id = NodeID.CDH

class SOTI:
    def __init__(self, write_queue, out_queue):
        self.write_msg_queue = write_queue
        self.out_msg_queue = out_queue
        self.sender_id = NodeID.CDH
        self.commands = {
            "send": self.do_send,
            "iamnow": self.do_iamnow,
            "help": self.do_help,
            "list": self.do_list,
            "exit": self.do_exit,
        }
        print("\nAvailable commands:\nsend\niamnow\nhelp\nlist\nexit\n")

    def do_send(self, arg):
        """Sends a command."""
        global enable_printing
        try:
            enable_printing.clear()

            msg = parser.parse_send(arg, self.sender_id)

            msg_yaml = dict_to_yaml(msg.as_dict(), 1, True)
            print(f"\nPreparing to send message:\n{msg_yaml}")

            match session.prompt("Send this message? (Y/N) ").lower():
                case "y":
                    # send the message to be written to the serial device and logged
                    self.write_msg_queue.put(msg)
                    self.out_msg_queue.put(msg)
                case _:
                    print("Cancelled message send.")

        except (ValueError, parser.ArgumentException) as e:
            print(e)
        
        finally:
            print()
            enable_printing.set()

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
        global do_exit
        do_exit = True

    def do(self, line):
        try:
            parts = shlex.split(line)
            if not parts:
                return
        except ValueError as e:
            print(e)
            return

        command = parts[0]
        arg = " ".join(parts[1:])

        func = self.commands.get(command)

        if func is None:
            print(f"Unknown command: {command}")
            return

        func(arg)


def print_messages(print_queue):
    while True:
        msg = print_queue.get()
        enable_printing.wait()
        print(msg, flush=True)


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
        print_queue = multiprocessing.Queue() # messages to be printed to CLI

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
                print_queue,
                stop_session_logger_flag,
                selected_port.device
            ),
            daemon=True)
        )

        # start the processes
        for p in processes:
            p.start()

        # create the printing thread
        threading.Thread(
            target=print_messages,
            args=(print_queue,),
            daemon=True,
        ).start()

        #CommandLine(out_msg_queue, write_msg_queue).cmdloop()

        cli = SOTI(write_msg_queue, out_msg_queue)

        session = PromptSession()

        with patch_stdout():
            while not do_exit:
                line = session.prompt("> ")

                if not line.strip():
                    continue

                cli.do(line)

    except KeyboardInterrupt:
        pass

    finally:
        # tell the processes to stop
        stop_serial_reader_flag.set()
        stop_session_logger_flag.set()

        for p in processes:
            p.join()

        print("\nExiting...")
