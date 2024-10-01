"""
The main soti front-end script which initializes the terminal and listener threads.
"""

import multiprocessing
import cmd
import json
import os
import serial.tools.list_ports

from utils import help_strings
from utils.constants import SAVE_DATA_DIR, NodeID, CmdID, COMM_INFO, MSG_HISTORY_PATH

from serial_reader import serial_reader
from message_parser import parser

# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class CommandLine(cmd.Cmd):
    """Represents the command line interface."""
    # initialize the object
    def __init__(self, out_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\nsetid\nquery\nclear\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_queue
        self.sender_id = NodeID.CDH


    def do_send(self, arg):
        """Sends a command."""
        args = arg.split()

        # first byte of the argument is the command code
        # (this operation grabs the "0x" prefix and first two hex digits)
        cmd_id = CmdID(int(args[0], 16))

        # now we can use the code to find its priority & destination id
        priority = COMM_INFO[cmd_id]["priority"]
        dest_id = COMM_INFO[cmd_id]["dest"]

        print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

        buffer = bytearray([priority, self.sender_id.value, dest_id.value, cmd_id.value, 0, 0, 0, 0, 0, 0, 0])

        # split arguments (if any) into independent bytes
        input_args = arg[4:]

        # pad input args with zeros to create a full message
        while len(input_args) < 14:
            input_args += "0"

        # fill the buffer with the input args
        position = 0
        for arg_byte in range(4,11):
            buffer[arg_byte] = int(input_args[position:position+2], 16)
            position += 2

        # send the command + arguments to the serial handler to write to the serial device
        self.out_msg_queue.put(buffer)


    def do_setid(self, arg):
        """Changes the sender ID."""
        try:
            node_id = NodeID(int(arg, 0))
            if node_id in NodeID:
                self.sender_id = node_id
                print(f"Updated sender ID to {self.sender_id.get_display_name()}.")
            else:
                print("Invalid sender ID.")
        except ValueError:
            print("Invalid args.")


    def do_query(self, arg):
        """Queries the telemetry."""
        print(f"\nSearching message history for {arg} commands...")

        with open(MSG_HISTORY_PATH, encoding="utf_8") as history:
            msgs = json.load(history)

        num_results = 0

        for msg in msgs:
            if msg["type"] == arg:
                num_results += 1
                print(msg)

        print(f"\nFound {num_results} results.\n")


    def do_clear(self, _):
        """Clears the json message history file."""
        with open(MSG_HISTORY_PATH, 'w', encoding="utf_8") as history:
            history.write("[]")
            history.flush()
        print("The json message history file has been cleared.\n")


    def do_help(self, _):
        """Displays the help string."""
        print(help_strings.HELP_MESSAGE)


    def do_list(self, _):
        """Lists the available CAN commands."""
        print(help_strings.COMMAND_LIST)


    def do_exit(self, _):
        """Exits the CLI."""
        print("\nExiting...")
        # Terminate all active child processes.
        active = multiprocessing.active_children()
        for child in active:
            child.terminate()
            child.join()
        print("Exited successfully.\n")
        return True


# ----------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------

def init_json():
    """Initializes the JSON file which logs all messages."""
    if not os.path.exists(SAVE_DATA_DIR):
        os.mkdir(SAVE_DATA_DIR)

    if (not os.path.exists(MSG_HISTORY_PATH)) or (os.path.getsize(MSG_HISTORY_PATH) == 0):
        with open(MSG_HISTORY_PATH, 'w', encoding="utf_8") as history:
            history.write("[]")


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
    multiprocessing.set_start_method('spawn')

    print(SPLASH)
    print("\nWelcome to the SOTI CLI!\n")

    print("Available serial ports:")

    ports = serial.tools.list_ports.comports()
    for port in sorted(ports):
        print(port.device + " - " + port.description)

    selected_port = input("\nEnter the port to receive messages from:")

    in_msg_queue = multiprocessing.Queue() # messages received from SOTI board
    out_msg_queue = multiprocessing.Queue() # messages to send to SOTI board

    init_json()

    serial_reader_proc = multiprocessing.Process(target=serial_reader, args=(in_msg_queue, out_msg_queue, selected_port))
    serial_reader_proc.start()

    parser_proc = multiprocessing.Process(target=parser, args=(in_msg_queue,))
    parser_proc.start()

    CommandLine(out_msg_queue).cmdloop()