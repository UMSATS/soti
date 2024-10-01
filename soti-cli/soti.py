'''
 * FILENAME: soti.py
 *
 * DESCRIPTION: The main soti front-end script which initializes the terminal and listener threads.
 * 
 * NOTES: Massive credit to Mia for implementing the SOTI front-end.
 *        The following code is heavily inspired from her initial C Shell program.
 * 
 * SERIAL MESSAGE FORMAT:
 *  - Byte 0: message priority
 *  - Byte 1: sender ID
 *  - Byte 2: destination ID
 *  - Byte 3: command
 *  - Bytes 4-10: data arguments
 *
 * AUTHORS:
 *  - Mia
 *  - Christina
 *  - Daigh
 *  - Arnav
 *
 * CREATED ON: Jan 31, 2024
'''


# ----------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------

import multiprocessing
import serial
import serial.tools.list_ports
import cmd
import datetime
import json
import os
from queue import Empty
from cli_utils import help_strings
from cli_utils.command_args import parse_args
from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    COMM_INFO,
    NodeID,
    CmdID
)


# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class Soti_CLI(cmd.Cmd):
    # initialize the object
    def __init__(self, out_msg_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\nsetid\nquery\nclear\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_msg_queue
        self.sender_id = NodeID.CDH

    # send a command
    def do_send(self, line):
        args = line.split()
        
        # first byte of the argument is the command code
		# (this operation grabs the "0x" prefix and first two hex digits)
        cmd_id = CmdID(int(args[0], 16))

		# now we can use the code to find its priority & destination id
        priority = COMM_INFO[cmd_id]["priority"]
        dest_id = COMM_INFO[cmd_id]["dest"]

        print(f"\nCommand: {cmd_id.name}\nDestination: {dest_id.name}")

        buffer = bytearray([priority, self.sender_id.value, dest_id.value, cmd_id.value, 0, 0, 0, 0, 0, 0, 0])

		# split arguments (if any) into independent bytes
        input_args = line[4:]

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

    # change the sender ID
    def do_setid(self, line):
        try:
            id = int(line, 0)
            if id in NodeID:
                self.sender_id = NodeID(id)
                print("Updated sender ID to {}.".format(self.sender_id.name))
            else:
                print("Invalid sender ID.")
        except ValueError:
            print("Invalid args.")

    # query the telemetry
    def do_query(self, line):
        print("\nSearching message history for {} commands...".format(line))

        with open(MSG_HISTORY_FILENAME) as history:
            msgs = json.load(history)

        num_results = 0

        for msg in msgs:
            if msg["type"] == line:
                num_results += 1
                print(msg)

        print("\nFound {} results.\n".format(num_results))

    # clear the json message history file
    def do_clear(self, line):
        with open(MSG_HISTORY_FILENAME, 'w') as history:
            history.write("[]")
            history.flush()
        print("The json message history file has been cleared.\n")
    
    # display the help string
    def do_help(self, line):
        print(help_strings.help_message)

    # list the available commands
    def do_list(self, line):
        print(help_strings.command_map)

    # exit the CLI
    def do_exit(self, line):
        print("\nSOTI Exit: In-progress.")
        # get & terminate all active child processes
        active = multiprocessing.active_children()
        for child in active:
            child.terminate()
            child.join()
        print("SOTI Exit: Success.\n")
        return True


# ----------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------

# initializes the JSON file which logs all messages
def init_json():
    if (not os.path.exists(MSG_HISTORY_FILENAME)) or (os.path.getsize(MSG_HISTORY_FILENAME) == 0):
        with open(MSG_HISTORY_FILENAME, 'w') as history:
            history.write("[]")

# converts bytes to a string
def bytes_to_string(msg):
    result = "0x"
    for byte in msg:
        bytestring = str(hex(byte))[2:]
        if len(bytestring) < 2:
            result += "0"
        result += bytestring
    return result

# handles incoming and outgoing serial messages
def serial_handler(in_msg_queue, out_msg_queue, soti_port):
    # use a write timeout of 1 second to avoid infinite blocking
    with serial.Serial(soti_port, baudrate=115200, write_timeout=1) as ser:
        while True:
            # check for incoming messages
            while ser.in_waiting >= MSG_SIZE:
                # block and read indefinitely, reading messages 11 bytes at a time
                new_msg = ser.read(MSG_SIZE)
                new_msg_hex = new_msg.hex()
                print(f"New Message: 0x{new_msg_hex}")
                in_msg_queue.put(new_msg)

            # check for outgoing messages
            try:
                # write the appropriate command + arguments to the serial device
                out_msg = out_msg_queue.get(block=False)
                print(f"Sending bytes to the satellite: 0x{out_msg.hex()}")
                ser.write(out_msg)
            except Empty:
                pass
            except serial.SerialTimeoutException:
                print("Send Fail: Serial write timed out.")
 
# gets messages from the incoming queue and parses them
def parser(in_msg_queue):
    while True:
        new_msg_raw = in_msg_queue.get()
        new_msg_json = parse(new_msg_raw)
        print(f"Message Parsed: {new_msg_json}")
        with open(MSG_HISTORY_FILENAME) as history:
            history_json = json.load(history)
        history_json.append(new_msg_json)
        with open(MSG_HISTORY_FILENAME, 'w') as history:
            json.dump(history_json, history, indent=4)

# parses a message
def parse(msg_raw):
    msg = bytes_to_string(msg_raw)
    comm_code = int(msg[8:10], 16)

    new_msg_json = {
        "time": datetime.datetime.now().strftime("%T"),
        "priority": int(msg[2:4], 16),
        "sender-id": NodeID(int(msg[4:6], 16)).name,
        "destination-id": NodeID(int(msg[6:8], 16)).name,
        "type": CmdID(comm_code).name,
        # the remaining attributes are command-specific,
        # and handled on case-by-case basis
    }

    parse_args(msg[8:], new_msg_json)

    return new_msg_json


# ----------------------------------------------------------
# PROGRAM SCRIPT
# ----------------------------------------------------------

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')

    # ascii art lol
    # font taken from https://patorjk.com/software/taag/
    print("\n_._*_   ________  __________ .__'_        _\n"
    "___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____\n"
    ".___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>\n"
    "_'._ /___/\\____/ /_/ /___/   *_.__       /_/\n")
    print("\nWelcome to the SOTI CLI!\n")

    print("Available serial ports:")

    PORTS = serial.tools.list_ports.comports()
    for PORT in sorted(PORTS):
        print(PORT.device + " - " + PORT.description)

    SOTI_PORT = input("\nEnter the port to receive messages from:")

    IN_MSG_QUEUE = multiprocessing.Queue() # messages recevied from SOTI back-end
    OUT_MSG_QUEUE = multiprocessing.Queue() # messages to send to SOTI back-end

    init_json()

    serial_handler_proc = multiprocessing.Process(target=serial_handler, args=(IN_MSG_QUEUE, OUT_MSG_QUEUE, SOTI_PORT))
    print("\nSerial Handler Status: Running")
    serial_handler_proc.start()

    parser_proc = multiprocessing.Process(target=parser, args=(IN_MSG_QUEUE,))
    print("Parser Status: Running")
    parser_proc.start()

    Soti_CLI(OUT_MSG_QUEUE).cmdloop()
