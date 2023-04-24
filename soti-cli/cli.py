import sys

# well-known help messages for commands
send_help = """
Send a command to the satellite.

Arguments:
-c, --code......The code for the command to send (REQUIRED)
-t, --time......The time to send the command (OPTIONAL; defaults to current time)
"""

query_help = """
Query the satellite for information.

Available subcommands:
charge........The charge state of the battery
comq..........The status of the command queue
pyld..........Science and ancillary data from the payload
telem.........Current or saved telemetry sensor data
"""

help_message = """
Use \"-h\" with any command for specific help.
send: sends a command to the board
query: retrieves information from the board
exit: exits the program
"""

def send_parse(args):
	args_dict = {
		"help": ("-h" in args or "--help" in args),
		"code": None,
		"time": None,
	}
	return args_dict

def query_parse(args):
	# TODO xor these subcommands
	args_dict = {
		"help": ("-h" in args or "--help" in args),
		"charge": ("charge" in args),
		"comq": ("comq" in args),
		"pyld": ("pyld" in args),
		"telem": ("telem" in args)
	}
	return args_dict

# subroutines to handle each user command
def send_command(args):
	if not args:
		print(send_help)
		return

	args_dict = send_parse(args)

	if args_dict["help"]:
		print(send_help)

def query_command(args):
	if not args:
		print(query_help)
		return

	args_dict = query_parse(args)

	if args_dict["help"]:
		print(query_help)

def help_command(*args):
	print(help_message);

def exit_command(*args):
	print("Exiting...")
	sys.exit(0)

# define commands that the user can use  in this application
commands = {
	"send": send_command,
	"query": query_command,
	"help": help_command,
	"exit": exit_command
}

print("Welcome to the SOTI CLI!\nOne day I'll put some ASCII art here like in the demo.")
print("Available commands:\nsend\nquery\nhelp\nexit")
print("Use \"-h\"/\"-help\" with any command for specifics.");

while True:
	try:
		line_in = input("> ")

	except KeyboardInterrupt:
		print("\nExiting...")
		sys.exit(0)

	args = None
	tokens_in = line_in.split(' ')
	comm = tokens_in[0]
	if len(tokens_in) > 1:
		args = tokens_in[1:]

	if comm in commands.keys():
		commands[comm](args)
	else:
		print("Command {} doesn't exist.\nUse \"help\" for a list of commands.".format(comm))
