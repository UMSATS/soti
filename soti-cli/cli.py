import argparse, sys
from cli_utils import help_strings

def send_command(args):
	print("sending")

def query_command(args):
	print("querying")

def help_command():
	print(help_strings.help_message)

parser = argparse.ArgumentParser(prog="", add_help=False)

subparsers_group = parser.add_subparsers(dest="command", help=help_strings.help_message)

send_subparser = subparsers_group.add_parser("send", description="sends a command to the satellite")
query_subparser = subparsers_group.add_parser("query", description="queries the satellite for information")
help_subparser = subparsers_group.add_parser("help")

send_subparser.add_argument("-c", "--code", type=int, required=True, help="the command code to send the satellite")
send_subparser.add_argument("-t", "--time", type=int, default=0, help="how many minutes in the future to send the command")

query_subparser.add_argument("attribute", choices=["charge", "comq", "pyld", "telem"], help="the attribute to query the satellite for")

args_fmtd = []
for arg in sys.argv[1:]:
	for arg_sub in arg.split():
		args_fmtd.append(arg_sub)

args = parser.parse_args(args_fmtd)

command = args.command
if command == "send":
	send_command(args)
elif command == "query":
	query_command(args)
elif command == "help":
	print(help_strings.help_message)

# for debugging
print(args)