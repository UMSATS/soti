from cli_utils.constants import CmdID

# well-known help messages for commands
help_message = """
send: sends a command to the satellite (input is hexadecimal, ex. 0xA1)
setid: sets the sender ID of sent commands
query: queries the satellite's message history for information
clear: clears the json message history file
help: displays this message
list: lists the available commands for each subsystem
exit: exits the program
"""

# formatted list of commands using CmdID enum
command_map = ""
command_map += "\nAvailable commands:\n\n=== Common ==="
current_subsystem = "COM"
for cmd in CmdID:
    name = cmd.name

    # add category header when subsystem changes
    subsystem = name[4:7]
    if subsystem != current_subsystem:
        current_subsystem = subsystem
        command_map += "\n\n=== "
        match subsystem:
            case 'CDH':
                command_map += "CDH"
            case 'PWR':
                command_map += "Power"
            case 'ADC':
                command_map += "ADCS"
            case 'PLD':
                command_map += "Payload"
        command_map += " ==="
    
    id = hex(cmd.value)
    # pad numbers less then 0x10 with a leading 0
    if len(id) < 4:
        id = id[:2] + "0" + id[2]
    # uppercase hex digits
    id = id[:2] + id[2:].upper()

    command_map += "\n{id}:\t{name}".format(id=id, name=name)

command_map += "\n"
