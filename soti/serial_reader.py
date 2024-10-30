"""Reads messages from the serial wire into a queue. Does not process them."""

from queue import Empty
import serial
from utils.constants import MSG_SIZE
from message import Message


def serial_reader(write_msg_queue, out_msg_queue, stop_pipe, soti_port):
    """Handles incoming and outgoing serial messages."""
    try:
        # use a write timeout of 1 second to avoid infinite blocking
        with serial.Serial(soti_port, baudrate=115200, write_timeout=1) as ser:
            while True:
                if stop_pipe.poll():
                    break

                # check for incoming messages
                while ser.in_waiting >= MSG_SIZE:
                    # block and read indefinitely, reading messages 11 bytes at a time
                    new_msg_bytes = ser.read(MSG_SIZE)
                    new_msg_hex = new_msg_bytes.hex()
                    print(f"New Message: 0x{new_msg_hex}")
                    new_msg = Message.deserialize(new_msg_bytes)
                    new_msg.source = "port"
                    write_msg_queue.put(new_msg)

                # check for outgoing messages
                try:
                    # write the appropriate command + arguments to the serial device
                    out_msg = out_msg_queue.get(block=False).serialize()
                    print(f"Sending bytes to the satellite: 0x{out_msg.hex().upper()}")
                    ser.write(out_msg)
                except Empty:
                    pass
                except serial.SerialTimeoutException:
                    print("Send Fail: Serial write timed out.")

    except KeyboardInterrupt:
        # abort the remaining messages
        while not out_msg_queue.empty():
            out_msg_queue.get()

    finally:
        stop_pipe.close()
