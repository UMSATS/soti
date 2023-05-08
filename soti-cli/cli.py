import argparse, sys
from cli_utils import help_strings

def send_command(args):
	print("sending")

def query_command(args):
	print("querying")

def help_command():
	print(help_strings.help_message)

parser = argparse.ArgumentParser()

subparsers_group = parser.add_subparsers(dest="command", help=help_strings.help_message)

send_subparser = subparsers_group.add_parser("send", help=help_strings.send_help)
query_subparser = subparsers_group.add_parser("query", help=help_strings.query_help)
query_subparser = subparsers_group.add_parser("help")

send_subparser.add_argument("-c", dest="code")
send_subparser.add_argument("-t")

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
	print(help_strings.query_help)