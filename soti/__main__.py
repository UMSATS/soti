"""
The main soti front-end script which initializes the terminal and listener threads.
"""

import multiprocessing
import cmd
import json
import os
import serial.tools.list_ports
import sys
import datetime

import serial.tools.list_ports_common

from utils import help_strings
from utils.constants import SAVE_DATA_DIR, NodeID, CmdID, COMM_INFO, MSG_HISTORY_PATH, SESSION_FILE_FORMAT

from serial_reader import serial_reader
from message_parser import parser

class ArgumentException(Exception): pass

# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class CommandLine(cmd.Cmd):
    """Represents the command line interface."""
    # initialize the object
    def __init__(self, out_queue, write_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\niamnow\nquery\nclear\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_queue
        self.write_msg_queue = write_queue
        self.sender_id = NodeID.CDH


    def do_send(self, arg):
        """Sends a command."""
        try:
            cmd_str, data, options, parse_error = parse_send(arg)
            
            # resolve command argument to corresponding ID
            try:
                cmd_id = CmdID(int(cmd_str, 16))
            except ValueError:
                if cmd_str in CmdID.__members__:
                    cmd_id = CmdID[cmd_str]
                else:
                    raise ArgumentException("Invalid command code")
            
            # get the default values for the command
            priority = COMM_INFO[cmd_id]["priority"]
            sender_id = self.sender_id
            dest_id = COMM_INFO[cmd_id]["dest"]
            
            # override defaults with optional arguments
            for key in options:
                if key == "priority":
                    priority = int(options["priority"])
                
                try:
                    if key == "from":
                        sender_id = NodeID[options["from"]]
                    if key == "to":
                        dest_id = NodeID[options["to"]]
                except KeyError:
                    raise ArgumentException("Invalid node ID")
            
            # raise exceptions for invalid arguments
            if parse_error:
                raise ArgumentException(parse_error)
            
            if not (0 <= priority <= 32):
                raise ArgumentException("Invalid priority")
            
            if dest_id is None:
                raise ArgumentException(f"{cmd_id.name} requires a recipient")

            # create buffer with empty payload
            buffer = bytearray([priority, sender_id.value, dest_id.value, cmd_id.value] + [0] * 7)

            if data:
                # pad data with zeros to create a full message
                data = data.ljust(14, "0")

                # fill the buffer with the data bytes
                position = 0
                for arg_byte in range(4,11):
                    buffer[arg_byte] = int(data[position:position+2], 16)
                    position += 2

            print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

            # send the command + arguments to the serial handler to write to the serial device
            self.out_msg_queue.put(buffer)
            self.write_msg_queue.put(buffer)

        except ArgumentException as e:
            print(e)
            return


    def do_iamnow(self, arg):
        """Changes the default sender ID."""
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

def init_json(port: str) -> str:
    """Initializes the file which logs the session."""
    if not os.path.exists(SAVE_DATA_DIR):
        os.mkdir(SAVE_DATA_DIR)

    session_start = datetime.datetime.now()
    file_format = session_start.strftime(SESSION_FILE_FORMAT)

    header = {
        "date": file_format.split("_")[0],
        "time": file_format.split("_")[1],
        "session-length": None,
        "port": port,
        "messages": []
    }

    file_name = f"{file_format}.txt"

    with open(SAVE_DATA_DIR / file_name, 'w', encoding="utf_8") as history:
        history.write(json.dumps(header))

    return file_name

def finalize_json(file_name):
    with open(SAVE_DATA_DIR / file_name, 'r', encoding="utf_8") as history:
        log = json.load(history)

    session_start = datetime.datetime.strptime(file_name.strip(".txt"), SESSION_FILE_FORMAT)
    total_seconds = int((datetime.datetime.now() - session_start).total_seconds())
    minutes, seconds = divmod(total_seconds, 60)

    log["session-length"] = f"{minutes:02d}:{seconds:02d}"

    with open(SAVE_DATA_DIR / file_name, 'w', encoding="utf_8") as history:
        json.dump(log, history, indent=4)  # Write back the updated JSON with indentation

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
                value = format(int(part, 16), 'x')
                # restore leading zeroes
                data += value.zfill(len(part) - (2 if '0x' in part else 0))
        except ValueError:
            error = f"Unknown argument '{part}'"
    
    return cmd_id, data, options, error


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

        output_file_name = init_json(selected_port.device)

        multiprocessing.set_start_method('spawn')
        write_msg_queue = multiprocessing.Queue() # messages to be written to file
        out_msg_queue = multiprocessing.Queue() # messages to send to SOTI board

        if not selected_port is virtual_port:
            multiprocessing.Process(target=serial_reader, args=(write_msg_queue, out_msg_queue, selected_port.device), daemon=True).start()
            multiprocessing.Process(target=parser, args=(write_msg_queue, output_file_name), daemon=True).start()

        CommandLine(out_msg_queue, write_msg_queue).cmdloop()

        finalize_json(output_file_name)

    except KeyboardInterrupt:
        pass

    print("\nExiting...")
