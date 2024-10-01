"""Includes strings used in help messages."""

from utils.constants import CmdID


HELP_MESSAGE = """
send: sends a command to the satellite (input is hexadecimal, ex. 0xA1)
setid: sets the sender ID of sent commands
query: queries the satellite's message history for information
clear: clears the json message history file
help: displays this message
list: lists the available commands for each subsystem
exit: exits the program
"""


def generate_command_list() -> str:
    """Generates a formatted list of commands based off the CmdID enum."""
    # Friendlier category names.
    category_names = {
        "COMM": "Common",
        "CDH": "CDH",
        "PWR": "Power",
        "ADCS": "ADCS",
        "PLD": "Payload"
    }

    command_list = "\nAvailable Commands:\n"
    current_category = None
    for cmd_id in CmdID:
        category = cmd_id.name.split('_', 1)[0] # Extract the prefix in the name.

        if category != current_category:
            current_category = category

            if category in category_names:
                category_name = category_names[category]
            else:
                category_name = category # Default to the prefix

            command_list += "\n=== " + category_name + " ===\n"

        hex_code = f'0x{cmd_id.value:02x}'
        command_list += f"{hex_code}:\t{cmd_id.name}\n"

    command_list += "\n"

    return command_list


COMMAND_LIST = generate_command_list()
