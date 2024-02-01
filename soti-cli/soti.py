'''
 * FILENAME: soti.py
 *
 * DESCRIPTION: The main soti front-end script which initializes the terminal and listener threads.
 * 
 * NOTES: Massive credit to Mia for implementing the SOTI front-end.
 *        The following code is heavily inspired from her initial C Shell program.
 *
 * AUTHORS:
 *  - Mia
 *  - Christina
 *  - Daigh
 *  - Arnav
 *
 * CREATED ON: Jan 31, 2024
'''

import multiprocessing
import serial.tools.list_ports

# ascii art lol
# font taken from https://patorjk.com/software/taag/
print("\n_._*_   ________  __________ .__'_        _\n"
"___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____\n"
".___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>\n"
"_'._ /___/\\____/ /_/ /___/   *_.__       /_/\n")
print("\nWelcome to the SOTI CLI!\n")

print("Available serial ports:")

ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

soti_port = input("\nEnter the port to receive messages from:")
