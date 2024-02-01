'''
 * FILENAME: soti.py
 *
 * DESCRIPTION: The main soti front-end script which initializes the terminal and listener threads.
 * 
 * NOTES: Massive credit to Mia for implementing the SOTI front-end.
 *        The following code is heavily inspired from her initial C Shell program.
 *
 * AUTHORS:
 *  - Mia
 *  - Christina
 *  - Daigh
 *  - Arnav
 *
 * CREATED ON: Jan 31, 2024
'''

import multiprocessing
import serial
import cmd
import argparse
import datetime
import json
import sys
from cli_utils import help_strings
from cli_utils.constants import COMM_INFO, MSG_HISTORY_FILENAME, SYSTEM_IDS, QUERY_ATTRS
from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS
)
from cli_utils.command_args import parsers, parse_generic

# ascii art lol
# font taken from https://patorjk.com/software/taag/
print("\n_._*_   ________  __________ .__'_        _\n"
"___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____\n"
".___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>\n"
"_'._ /___/\\____/ /_/ /___/   *_.__       /_/\n")
print("\nWelcome to the SOTI CLI!\n")

print("Available serial ports:")

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

soti_port = input("\nEnter the port to receive messages from:")

try:
    init_json()
    main_loop_listener()
    main_loop_parser()
except:
    print("\nTelemetry listener exiting…")
    sys.exit(0)


# cli.py
parser = argparse.ArgumentParser(prog="", add_help=False)

subparsers_group = parser.add_subparsers(dest="operation", help="the available SOTI operations")

send_subparser = subparsers_group.add_parser("send", description="sends a command to the satellite")
query_subparser = subparsers_group.add_parser("query", description="queries the satellite's message history for information")
list_subparser = subparsers_group.add_parser("list", description="lists the available commands for each subsystem")
help_subparser = subparsers_group.add_parser("help", add_help=False)
exit_subparser = subparsers_group.add_parser("exit", add_help=False)

send_subparser.add_argument("command", type=str, help="the command code and arguments to send to the satellite, as an 8-bit hexadecimal number")

query_subparser.add_argument("attribute", choices=QUERY_ATTRS.values(), help="the attribute to query the satellite's message history for")

# use a default read timeout of 1 second to avoid infinite blocking
with serial.Serial(soti_port, baudrate=115200, timeout=1) as ser:
	args_raw = []
	for arg in sys.argv[2:]:
		for arg_sub in arg.split():
			args_raw.append(arg_sub)

	args = parser.parse_args(args_raw)

	operation = args.operation
	if operation == "send":

		# first byte of the argument is the command code
		# (this operation grabs the "0x" prefix and first two hex digits)
		code = int(args.command[0:4], 16)

		# now we can use the code to find its priority & destination id
		priority = COMM_INFO[code]["priority"]
		dest_id = COMM_INFO[code]["dest"]

		print(f"Command: {COMM_INFO[code]['name']}\nDestination: {SYSTEM_IDS[COMM_INFO[code]['dest']]}")

		buffer = bytearray([priority, 0x1, dest_id, code, 0, 0, 0, 0, 0, 0, 0])

		# split arguments (if any) into independent bytes
		input_args = args.command[4:]

		# pad input args to an even number of bytes to avoid trailing 0 issues
		if len(input_args) % 2:
			input_args += "0"

		# position variable tracks how much of the supplied command string we've parsed
		# it should increment by 2, as two characters = 1 byte
		pos = 0
		print(input_args)
		for arg_byte in range(4, 9):
			if pos < len(input_args):
				buffer[arg_byte] = int(f"0x{input_args[pos:pos+2]}", 16)
				pos += 2


		# write the appropriate command + arguments to the serial device
		print(f"Sending bytes to the satellite: {buffer.hex()}")
		ser.write(buffer)

	elif operation == "query":
		print("\nSearching message history for {} data…\n".format(args.attribute))
		msg_history = open(MSG_HISTORY_FILENAME)
		msgs = json.loads(msg_history.read())

		num_results = 0

		for msg in msgs:
			if msg["type"] == args.attribute:
				num_results += 1
				print(msg)

		print("\nFound {} results.".format(num_results))

	elif operation == "help":
		parser.print_help()

	elif operation == "list":
		print(help_strings.command_map)

	# exit is actually handled by the C shell, but we include it here for the facade of a CLI
	elif operation == "exit":
		pass

# listener.py
def bytes_to_string(msg):
    result = "0x"
    for byte in msg:
        bytestring = str(hex(byte))[2:]
        if len(bytestring) < 2:
            result += "0"
        result += bytestring
    return result

def parse(msg_raw):
    msg = bytes_to_string(msg_raw)
    comm_code = int(f"0x{msg[8:10]}", 16)

    new_msg_json = {
        "time": datetime.datetime.now().strftime("%T"),
        "priority": int(f"0x{msg[2:4]}", 16),
        "sender-id": SYSTEM_IDS[int(f"0x{msg[4:6]}", 16)],
        "destination-id": SYSTEM_IDS[int(f"0x{msg[6:8]}", 16)],
        "type": QUERY_ATTRS.get(comm_code) or "other-message",
        # the remaining attributes are command-specific,
        # and handled on case-by-case basis
    }

    if new_msg_json["type"] == "other-message":
        new_msg_json["command-code"] = f"0x{msg[8:10]}"

    if comm_code in parsers.keys():
        new_msg_json = parsers[comm_code](msg[10:], new_msg_json)
    else:
        new_msg_json = parse_generic(msg[10:], new_msg_json)

    return new_msg_json

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

def init_json():
    with open(MSG_HISTORY_FILENAME, "r+") as history:
        if not history.read():
            history.write("[]")

def main_loop_listener():
    print("Running")
    with serial.Serial(port_arg, baudrate=115200) as ser:
        while True:
            # block and read indefinitely, reading messages 11 bytes at a time
            new_msg = ser.read(MSG_SIZE)

            print(f"New Message: {new_msg.hex()}")

            new_msg_json = parse(new_msg)

            print(f"Message Parsed: {new_msg_json}")

            if new_msg_json:
                with open(MSG_HISTORY_FILENAME) as history:
                    contents = json.load(history)
                    contents.append(new_msg_json)
                with open(MSG_HISTORY_FILENAME, 'w') as history:
                    json.dump(contents, history, indent=4)

# parser.py
def bytes_to_string(msg):
    result = "0x"
    for byte in msg:
        bytestring = str(hex(byte))[2:]
        if len(bytestring) < 2:
            result += "0"
        result += bytestring
    return result

def parse(msg_raw):
    msg = bytes_to_string(msg_raw)
    comm_code = int(f"0x{msg[8:10]}", 16)

    new_msg_json = {
        "time": datetime.datetime.now().strftime("%T"),
        "priority": int(f"0x{msg[2:4]}", 16),
        "sender-id": SYSTEM_IDS[int(f"0x{msg[4:6]}", 16)],
        "destination-id": SYSTEM_IDS[int(f"0x{msg[6:8]}", 16)],
        "type": QUERY_ATTRS.get(comm_code) or "other-message",
        # the remaining attributes are command-specific,
        # and handled on case-by-case basis
    }

    if new_msg_json["type"] == "other-message":
        new_msg_json["command-code"] = f"0x{msg[8:10]}"

    if comm_code in parsers.keys():
        new_msg_json = parsers[comm_code](msg[10:], new_msg_json)
    else:
        new_msg_json = parse_generic(msg[10:], new_msg_json)

    return new_msg_json

def init_json():
    with open(MSG_HISTORY_FILENAME, "r+") as history:
        if not history.read():
            history.write("[]")

def main_loop_parser():
    while True:
        try:
            new_msg_raw = msg_queue.get()
            new_msg_json = parse(msg_queue.get())
            print(new_msg_json)
        
            print(f"Message Parsed: {new_msg_json}")
        
            if new_msg_json:
                with open(MSG_HISTORY_FILENAME) as history:
                    contents = json.load(history)
                    contents.append(new_msg_json)
                with open(MSG_HISTORY_FILENAME, 'w') as history:
                    json.dump(contents, history, indent=4)
        except msg_queue.empty():
            pass

