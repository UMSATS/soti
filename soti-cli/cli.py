import argparse, serial, sys
from cli_utils import command_codes, help_strings

def help_command():
	print(help_strings.help_message)

parser = argparse.ArgumentParser(prog="", add_help=False)

subparsers_group = parser.add_subparsers(dest="command", help="the available SOTI commands")

send_subparser = subparsers_group.add_parser("send", description="sends a command to the satellite")
query_subparser = subparsers_group.add_parser("query", description="queries the satellite for information")
help_subparser = subparsers_group.add_parser("help", add_help=False)
exit_subparser = subparsers_group.add_parser("exit", add_help=False)

# TODO let this accept base 16 ints
send_subparser.add_argument("-c", "--code", type=int, required=True, help="the command code to send the satellite")
send_subparser.add_argument("-t", "--time", type=int, default=0, help="the timestamp to send the command at")

query_subparser.add_argument("attribute", choices=command_codes.QCC_MAP.keys(), help="the attribute to query the satellite for")

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
	data_out = ""

	command = args.command
	if command == "send":
		# TODO checking if time-tagging is required will occur here!

		# write the appropriate command to the serial device
		ser.write(args.code)

		# record the response
		# TODO how much data do we expect to read from each command?
		data_out = ser.read()

		# add further processing of output if necessary
	elif command == "query":
		print(command_codes.QCC_MAP[args.attribute])
		ser.read()
		
		# add further processing of output if necessary
	elif command == "help":
		parser.print_help()
	# actually handled by the C shell, but we include it here for the facade of a CLI
	elif command == "exit":
		pass

	# for debugging
	print(args)
	print("Send to: ", ser.name)