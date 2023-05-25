import argparse, json, serial, sys
from cli_utils import help_strings
from cli_utils.constants import COMM_PRIORITIES, MSG_HISTORY_FILENAME, QUERY_ATTRS, hexint

MSG_SIZE = 10

parser = argparse.ArgumentParser(prog="", add_help=False)

subparsers_group = parser.add_subparsers(dest="operation", help="the available SOTI operations")

send_subparser = subparsers_group.add_parser("send", description="sends a command to the satellite", help=help_strings.command_map)
query_subparser = subparsers_group.add_parser("query", description="queries the satellite's message history for information")
help_subparser = subparsers_group.add_parser("help", add_help=False)
exit_subparser = subparsers_group.add_parser("exit", add_help=False)

send_subparser.add_argument("command", type=hexint, help="the command code and arguments to send to the satellite, as an 8-bit hexadecimal number")

query_subparser.add_argument("attribute", choices=QUERY_ATTRS.values(), help="the attribute to query the satellite's message history for")

# first script argument will be the device to read/write to
port_arg = sys.argv[1]

# debug: provide an empty string and we create an unopened serial connection
if not port_arg:
	port_arg = None

# use a default read timeout of 1 second to avoid infinite blocking
with serial.Serial(port_arg, baudrate=115200, timeout=1) as ser:
	args_raw = []
	for arg in sys.argv[2:]:
		for arg_sub in arg.split():
			args_raw.append(arg_sub)

	args = parser.parse_args(args_raw)

	operation = args.operation
	if operation == "send":
		# first two bytes of the argument are the command code
		code = (args.command & (0xFF00)) >> 8

		# TODO format the argument properly to send to the satellite

		# write the appropriate command + arguments to the serial device
		print(code)

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

	# exit is actually handled by the C shell, but we include it here for the facade of a CLI
	elif operation == "exit":
		pass

	# for debugging
	print(args)
	print("Send to: ", ser.name)