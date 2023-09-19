import argparse, json, serial, sys
from cli_utils import help_strings
from cli_utils.constants import COMM_INFO, MSG_HISTORY_FILENAME, SYSTEM_IDS, QUERY_ATTRS

parser = argparse.ArgumentParser(prog="", add_help=False)

subparsers_group = parser.add_subparsers(dest="operation", help="the available SOTI operations")

send_subparser = subparsers_group.add_parser("send", description="sends a command to the satellite")
query_subparser = subparsers_group.add_parser("query", description="queries the satellite's message history for information")
list_subparser = subparsers_group.add_parser("list", description="lists the available commands for each subsystem")
help_subparser = subparsers_group.add_parser("help", add_help=False)
exit_subparser = subparsers_group.add_parser("exit", add_help=False)

send_subparser.add_argument("command", type=str, help="the command code and arguments to send to the satellite, as an 8-bit hexadecimal number")

query_subparser.add_argument("attribute", choices=QUERY_ATTRS.values(), help="the attribute to query the satellite's message history for")

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

# use a default read timeout of 1 second to avoid infinite blocking
with serial.Serial(port_arg, baudrate=115200, timeout=1) as ser:
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