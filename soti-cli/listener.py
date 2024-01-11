from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS
)

from cli_utils.command_args import parsers, parse_generic

from shared_queue import msg_queue

import json, serial, sys, datetime, queue, time

# first script argument will be the device to read/write to
#port_arg = sys.argv[1]
port_arg = "/dev/tty.Bluetooth-Incoming-Port"  

def listen():
    print("Running")
    with serial.Serial(port_arg, baudrate=115200) as ser:
        while True:
            # block and read indefinitely, reading messages 11 bytes at a time
             #new_msg = ser.read(MSG_SIZE)
             new_msg = bytes(11)
             msg_queue.put(new_msg)
             print(f"New Message: {new_msg.hex()}")
             time.sleep(1)

if __name__ == "__main__":
    listen()
