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
from utils.constants import SESSIONS_DIR, NodeID, CmdID, COMM_INFO, SESSION_FILE_FORMAT

from serial_reader import serial_reader
from message_parser import log_messages, dict_to_yaml, Message

class ArgumentException(Exception): pass

# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class CommandLine(cmd.Cmd):
    """Represents the command line interface."""
    # initialize the object
    def __init__(self, out_queue, write_queue, output_file_name):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\niamnow\nquery\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_queue
        self.write_msg_queue = write_queue
        self.file_name = output_file_name
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

            msg = Message(buffer)

            print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.get_display_name()}")

            # send the command + arguments to the serial handler to write to the serial device
            self.out_msg_queue.put(msg)
            self.write_msg_queue.put(msg)

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
        """Queries the message history by command name."""
        print(f"\nSearching message history for {arg} commands...")

        with open(SESSIONS_DIR / self.file_name, encoding="utf_8") as history:
            log = history.read()

        num_results = 0

        lines = log.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("cmd: ") and line[5:] == arg:
                num_results += 1

        print(f"\nFound {num_results} results.\n")


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

def init_session_log(port: str) -> str:
    """Initializes the file which logs the session."""
    if not os.path.exists(SESSIONS_DIR):
        os.mkdir(SESSIONS_DIR)

    session_start = datetime.datetime.now()

    file_format = session_start.strftime(SESSION_FILE_FORMAT)
    file_name = f"{file_format}.log"

    date = session_start.strftime("%Y-%m-%d")
    time = session_start.strftime("%H:%M:%S")

    header_dict = {
        "date": date,
        "time": time,
        "session-length": None,
        "port": port,
        "messages": ""
    }

    header = dict_to_yaml(header_dict, 0)

    with open(SESSIONS_DIR / file_name, 'w', encoding="utf_8") as history:
        history.write(header)

    return file_name

def finalize_session_log(file_name):
    """Writes the session length to the log file."""
    with open(SESSIONS_DIR / file_name, encoding="utf_8") as history:
        log = history.read()

    # get the datetime corresponding to the file name
    session_start = datetime.datetime.strptime(file_name.strip(".log"), SESSION_FILE_FORMAT)

    total_seconds = int((datetime.datetime.now() - session_start).total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # conditionally add hours and format the time
    log = log.split("\n")
    hours_str = f"{hours:02d}:" if hours else ""
    log[2] = f"session-length: '{hours_str}{minutes:02d}:{seconds:02d}'"
    log = "\n".join(log)

    with open(SESSIONS_DIR / file_name, 'w', encoding="utf_8") as history:
        history.write(log)

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

        output_file_name = init_session_log(selected_port.device)

        multiprocessing.set_start_method('spawn')
        write_msg_queue = multiprocessing.Queue() # messages to be written to file
        out_msg_queue = multiprocessing.Queue() # messages to send to SOTI board

        if selected_port is not virtual_port:
            multiprocessing.Process(target=serial_reader, args=(write_msg_queue, out_msg_queue, selected_port.device), daemon=True).start()
        
        multiprocessing.Process(target=log_messages, args=(write_msg_queue, output_file_name), daemon=True).start()

        CommandLine(out_msg_queue, write_msg_queue, output_file_name).cmdloop()

        finalize_session_log(output_file_name)

    except KeyboardInterrupt:
        pass

    print("\nExiting...")
