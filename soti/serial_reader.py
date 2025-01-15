"""Reads messages from the serial wire into a queue. Does not process them."""

from queue import Empty
import serial
from utils.constants import MSG_SIZE
from message import Message


def serial_reader(write_msg_queue, out_msg_queue, stop_flag, port):
    """Handles incoming and outgoing serial messages."""
    try:
        # use a write timeout of 1 second to avoid infinite blocking
        with serial.Serial(port, baudrate=115200, write_timeout=1) as ser:
            while not stop_flag.is_set():
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
                    out_msg = out_msg_queue.get(block=False)

                    out_msg_cmd = out_msg.as_dict()["cmd"].name
                    out_msg_recipient = out_msg.as_dict()["recipient-id"].get_display_name()
                    print(f"Sending '{out_msg_cmd}' to {out_msg_recipient}.")

                    # write the message to the serial device
                    ser.write(out_msg.serialize())
                except Empty:
                    pass
                except serial.SerialTimeoutException:
                    print("Send Fail: Serial write timed out.")
    except KeyboardInterrupt:
        pass