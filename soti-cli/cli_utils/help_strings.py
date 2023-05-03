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
