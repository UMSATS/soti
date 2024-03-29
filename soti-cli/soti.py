'''
 * FILENAME: soti.py
 *
 * DESCRIPTION: The main soti front-end script which initializes the terminal and listener threads.
 * 
 * NOTES: Massive credit to Mia for implementing the SOTI front-end.
 *        The following code is heavily inspired from her initial C Shell program.
 * 
 * SERIAL MESSAGE FORMAT:
 *  - Byte 0: message priority
 *  - Byte 1: sender ID
 *  - Byte 2: destination ID
 *  - Byte 3: command
 *  - Bytes 4-10: data arguments
 *
 * AUTHORS:
 *  - Mia
 *  - Christina
 *  - Daigh
 *  - Arnav
 *
 * CREATED ON: Jan 31, 2024
'''


# ----------------------------------------------------------
# IMPORTS
# ----------------------------------------------------------

import multiprocessing
import serial
import serial.tools.list_ports
import cmd
import datetime
import json
import os
from queue import Empty
from cli_utils import help_strings
from cli_utils.command_args import parsers, parse_generic
from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    CAMERA_DATA_FILENAME,
    CAMERA_IMAGE_FILENAME,
    MSG_SIZE,
    SOTI_SENDER_ID,
    COMM_INFO,
    SYSTEM_IDS,
    QUERY_ATTRS
)


# ----------------------------------------------------------
# CMD CLASS
# ----------------------------------------------------------

class Soti_CLI(cmd.Cmd):
    # initialize the object
    def __init__(self, out_msg_queue):
        super().__init__()
        self.intro = "\nAvailable commands:\nsend\nquery\nextract\nclearj\nclearc\nhelp\nlist\nexit\n"
        self.prompt = ">> "
        self.out_msg_queue = out_msg_queue

    # send a command
    def do_send(self, line):
        # first byte of the argument is the command code
		# (this operation grabs the "0x" prefix and first two hex digits)
        code = int(line[0:4], 16)

		# now we can use the code to find its priority & destination id
        priority = COMM_INFO[code]["priority"]
        dest_id = COMM_INFO[code]["dest"]

        print(f"\nCommand: {COMM_INFO[code]['name']}\nDestination: {SYSTEM_IDS[dest_id]}")

        buffer = bytearray([priority, SOTI_SENDER_ID, dest_id, code, 0, 0, 0, 0, 0, 0, 0])

		# split arguments (if any) into independent bytes
        input_args = line[4:]

        # pad input args with zeros to create a full message
        while len(input_args) < 14:
            input_args += "0"
        
        # fill the buffer with the input args
        position = 0
        for arg_byte in range(4,11):
            buffer[arg_byte] = int(f"0x{input_args[position:position+2]}", 16)
            position += 2

        # send the command + arguments to the serial handler to write to the serial device
        self.out_msg_queue.put(buffer)

    # query the telemetry
    def do_query(self, line):
        print("\nSearching message history for {} data…".format(line))

        with open(MSG_HISTORY_FILENAME) as history:
            msgs = json.load(history)

        num_results = 0

        for msg in msgs:
            if msg["type"] == line:
                num_results += 1
                print(msg)

        print("\nFound {} results.\n".format(num_results))

    # extract the jpeg image from the txt camera data
    def do_extract(self, line):
        extract()

    # clear the json message history file
    def do_clearj(self, line):
        with open(MSG_HISTORY_FILENAME, 'w') as history:
            history.write("[]")
            history.flush()
        print("The json message history file has been cleared.\n")

    # clear the txt camera data file
    def do_clearc(self, line):
        with open(CAMERA_DATA_FILENAME, "w") as camera_data:
            camera_data.flush()
        print("The txt camera data file has been cleared.\n")
    
    # display the help string
    def do_help(self, line):
        print(help_strings.help_message)

    # list the available commands
    def do_list(self, line):
        print(help_strings.command_map)

    # exit the CLI
    def do_exit(self, line):
        print("\nSOTI Exit: In-progress.")
        # get & terminate all active child processes
        active = multiprocessing.active_children()
        for child in active:
            child.terminate()
            child.join()
        print("SOTI Exit: Success.\n")
        return True


# ----------------------------------------------------------
# FUNCTIONS
# ----------------------------------------------------------

# initializes the JSON file which logs all messages
def init_json():
    if (not os.path.exists(MSG_HISTORY_FILENAME)) or (os.path.getsize(MSG_HISTORY_FILENAME) == 0):
        with open(MSG_HISTORY_FILENAME, 'w') as history:
            history.write("[]")

# converts bytes to a string
def bytes_to_string(msg):
    result = "0x"
    for byte in msg:
        bytestring = str(hex(byte))[2:]
        if len(bytestring) < 2:
            result += "0"
        result += bytestring
    return result

# handles incoming and outgoing serial messages
def serial_handler(in_msg_queue, out_msg_queue, soti_port):
    # use a write timeout of 1 second to avoid infinite blocking
    with serial.Serial(soti_port, baudrate=115200, write_timeout=1) as ser:
        while True:
            # check for incoming messages
            while ser.in_waiting >= MSG_SIZE:
                # block and read indefinitely, reading messages 11 bytes at a time
                new_msg = ser.read(MSG_SIZE)
                new_msg_hex = new_msg.hex()
                if new_msg_hex[8:10] != "45": # don't print camera data
                    print(f"New Message: 0x{new_msg_hex}")
                in_msg_queue.put(new_msg)

            # check for outgoing messages
            try:
                # write the appropriate command + arguments to the serial device
                out_msg = out_msg_queue.get(block=False)
                print(f"Sending bytes to the satellite: 0x{out_msg.hex()}")
                ser.write(out_msg)
            except Empty:
                pass
            except serial.SerialTimeoutException:
                print("Send Fail: Serial write timed out.")
 
# gets messages from the incoming queue and parses them
def parser(in_msg_queue):
    with open(CAMERA_DATA_FILENAME, "w") as camera_data:
        while True:
            new_msg_raw = in_msg_queue.get()
            new_msg_hex = new_msg_raw.hex()

            if new_msg_hex[8:10] == "45": # if the new message is camera data
                camera_data.write(new_msg_hex + "\n")
                camera_data.flush()
            else:
                new_msg_json = parse(new_msg_raw)
                print(f"Message Parsed: {new_msg_json}")
                with open(MSG_HISTORY_FILENAME) as history:
                    history_json = json.load(history)
                history_json.append(new_msg_json)
                with open(MSG_HISTORY_FILENAME, 'w') as history:
                    json.dump(history_json, history, indent=4)

# parses a message
def parse(msg_raw):
    msg = bytes_to_string(msg_raw)
    comm_code = int(f"0x{msg[8:10]}", 16)

    new_msg_json = {
        "time": datetime.datetime.now().strftime("%T"),
        "priority": int(f"0x{msg[2:4]}", 16),
        "sender-id": SYSTEM_IDS[int(f"0x{msg[4:6]}", 16)],
        "destination-id": SYSTEM_IDS[int(f"0x{msg[6:8]}", 16)],
        "type": QUERY_ATTRS.get(comm_code) or "other-message",
        # the remaining attributes are command-specific,
        # and handled on case-by-case basis
    }

    if comm_code in parsers.keys():
        new_msg_json = parsers[comm_code](msg[10:], new_msg_json)
    else:
        new_msg_json = parse_generic(msg[8:], new_msg_json)

    return new_msg_json

# extract the jpeg image from the txt camera data
def extract():
    camera_data_dict = {}

    # build the camera data dictionary
    with open(CAMERA_DATA_FILENAME, "r") as input_file:
        for line in input_file:
            line = line.strip('\x00')
            index = int(line[10:14], 16)
            if index not in camera_data_dict:
                camera_data_dict[index] = line[14:].strip()
            else:
                print("Duplicate camera message detected with index: " + index)
    
    if int("ffff", 16) not in camera_data_dict: # check if termination message was captured
        print("Error: Camera data capture was incomplete.")
        print("Unable to produce an image.")
    else: # write the camera data to a file
        camera_data_dict.pop(int("ffff", 16)) # remove the termination messsage
        
        image_index = 0
        while os.path.exists(CAMERA_IMAGE_FILENAME[:9] + str(image_index) + CAMERA_IMAGE_FILENAME[9:]):
            image_index += 1
        
        file_to_create = CAMERA_IMAGE_FILENAME[:9] + str(image_index) + CAMERA_IMAGE_FILENAME[9:]
        with open(file_to_create, "wb") as output_file:
            final_index = max(camera_data_dict)
            for i in range(final_index + 1):
                if i in camera_data_dict:
                    data_bytes = bytes.fromhex(camera_data_dict[i])
                    output_file.write(data_bytes)
                else:
                    print("Camera data package missing with index: " + str(i))

        print("\nImage processing complete.\n")


# ----------------------------------------------------------
# PROGRAM SCRIPT
# ----------------------------------------------------------

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')

    # ascii art lol
    # font taken from https://patorjk.com/software/taag/
    print("\n_._*_   ________  __________ .__'_        _\n"
    "___*   / __/ __ \\/_  __/  _/   __*'.     \\ \\_____\n"
    ".___  _\\ \\/ /_/ / / / _/ /    '__*.   ###[==_____>\n"
    "_'._ /___/\\____/ /_/ /___/   *_.__       /_/\n")
    print("\nWelcome to the SOTI CLI!\n")

    print("Available serial ports:")

    PORTS = serial.tools.list_ports.comports()
    for PORT in sorted(PORTS):
        print(PORT.device + " - " + PORT.description)

    SOTI_PORT = input("\nEnter the port to receive messages from:")

    IN_MSG_QUEUE = multiprocessing.Queue() # messages recevied from SOTI back-end
    OUT_MSG_QUEUE = multiprocessing.Queue() # messages to send to SOTI back-end

    init_json()

    serial_handler_proc = multiprocessing.Process(target=serial_handler, args=(IN_MSG_QUEUE, OUT_MSG_QUEUE, SOTI_PORT))
    print("\nSerial Handler Status: Running")
    serial_handler_proc.start()

    parser_proc = multiprocessing.Process(target=parser, args=(IN_MSG_QUEUE,))
    print("Parser Status: Running")
    parser_proc.start()

    Soti_CLI(OUT_MSG_QUEUE).cmdloop()
