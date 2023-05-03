from pynput import keyboard
import sys

from cli_utils import help_strings

input_buffer = ""

def get_history():
	print("getting history")

def on_key_pressed(key):
	print("Pressed key {}".format(key))
	if key == keyboard.Key.up:
		get_history()

def on_key_released(key):
	print("Released key {}".format(key))
	if key == keyboard.Key.enter:
		print("return all input")

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
		print(help_strings.send_help)
		return

	args_dict = send_parse(args)

	if args_dict["help"]:
		print(help_strings.send_help)

def query_command(args):
	if not args:
		print(help_strings.query_help)
		return

	args_dict = query_parse(args)

	if args_dict["help"]:
		print(help_strings.query_help)

def help_command(*args):
	print(help_strings.help_message)

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

def main_loop():
	while True:
		# TODO use pynput to get input lines to not fuck with the arrowkeys
		pass


		# args = None
		# tokens_in = line_in.split(' ')
		# comm = tokens_in[0]
		# if len(tokens_in) > 1:
		# 	args = tokens_in[1:]

		# if comm in commands.keys():
		# 	commands[comm](args)
		# else:
		# 	print("Command {} doesn't exist.\nUse \"help\" for a list of commands.".format(comm))

if __name__ == '__main__':
	listener = keyboard.Listener(on_press=on_key_pressed, on_release=on_key_released)
	print("Welcome to the SOTI CLI!\nOne day I'll put some ASCII art here like in the demo.")
	print("Available commands:\nsend\nquery\nhelp\nexit")
	print("Use \"-h\"/\"-help\" with any command for specifics.")

	listener.start()
	try:
		main_loop()

	except KeyboardInterrupt:
		print("\nExiting...")
		sys.exit(0)
