from cli_utils.constants import (
    MSG_HISTORY_FILENAME,
    MSG_SIZE,
    QUERY_ATTRS,
    SYSTEM_IDS
)

from cli_utils.command_args import parsers, parse_generic

#from shared_queue import msg_queue

import json, sys, datetime, queue, time, redis
import serial

r = redis.Redis(host="localhost", port=6379, db=0)
r.mset({"byte0":"", "byte1":"", "byte2":"", "byte3":"", "byte4":"", "byte5":"", "byte6":"", "byte7":"", 
        "byte8":"", "byte9":"", "byte10":"", "byte11":""})

msg_queue = queue.Queue()

# first script argument will be the device to read/write to
#port_arg = sys.argv[1]
port_arg = "/dev/tty.Bluetooth-Incoming-Port"
new_msg = [] 
data = []  

ser = serial.Serial(port_arg, baudrate=115200)

def listen():
    print("Running")
    while True:
        # block and read indefinitely, reading messages 11 bytes at a time
        
        new_msg = bytes(11)
        
        for i in range(11):
            r.set("byte{number}".format(number=str(i)), new_msg[i])
        
        data.append(new_msg)

        msg_queue.put(new_msg)
        print(f"New Message: {new_msg.hex()}")
        time.sleep(1)

if __name__ == "__main__":
    listen()
