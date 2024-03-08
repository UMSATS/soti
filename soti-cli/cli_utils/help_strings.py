# well-known help messages for commands
help_message = """
send: sends a command to the satellite (input is hexadecimal, ex. 0xA1)
query: queries the satellite's message history for information
extract: extracts the jpeg image from the txt camera data file
clearj: clears the json message history file
clearc: clears the txt camera data file
help: displays this message
list: lists the available commands for each subsystem
exit: exits the program
"""

command_map = """
Available commands:

=== Common ===
0x01 ack
0x02 nack

=== CDH ===
0x33 process algae well light level
0x34 process algae well temperature
0x40 STM32 reset (CDH)
0x41 flash storage unit test
0x42 mram unit test
0x43 antenna spam deploy 1
0x44 antenna spam deploy 2
0x45 take picture

=== PLD ===
0xA0 STM32 reset (PLD)
0xA1 led on
0xA2 led off
0xA3 thermoregulation on
0xA4 thermoregulation off
0xA5 heater on
0xA6 heater off

== ACDS ===
0xB0 STM32 reset (ACDS)
0xB1 magnetorquer 1 full strength
0xB2 magnetorquer 2 full strength
0xB3 magnetorquer 3 full strength
0xB4 magnetorquer 1 off
0xB5 magnetorquer 2 off
0xB6 magnetorquer 3 off
0xB7 magnetorquer 1 forward
0xB8 magnetorquer 2 forward
0xB9 magnetorquer 3 forward
0xBA magnetorquer 1 reverse
0xBB magnetorquer 2 reverse
0xBC magnetorquer 3 reverse
"""
