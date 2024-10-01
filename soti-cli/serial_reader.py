"""Reads messages from the serial wire into a queue. Does not process them."""

from queue import Empty
import serial
from cli_utils.constants import *


def serial_reader(in_msg_queue, out_msg_queue, soti_port):
    """Handles incoming and outgoing serial messages."""
    print("\nSerial Handler Status: Running")
    # use a write timeout of 1 second to avoid infinite blocking
    with serial.Serial(soti_port, baudrate=115200, write_timeout=1) as ser:
        while True:
            # check for incoming messages
            while ser.in_waiting >= MSG_SIZE:
                # block and read indefinitely, reading messages 11 bytes at a time
                new_msg = ser.read(MSG_SIZE)
                new_msg_hex = new_msg.hex()
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
