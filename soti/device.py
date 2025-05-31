import multiprocessing
import queue

import serial

import config
from utils.constants import MSG_SIZE
from message import Message

class Device:
    def __init__(self, name: str, description: str, icon: str = config.ICONS['PORT_DEFAULT']):
        self.name = name
        self.description = description
        self.icon = icon

    def stream_loop(self, stop_flag, read_queue: multiprocessing.Queue, write_queue: multiprocessing.Queue):
        try:
            while not stop_flag.is_set():
                # Clear write queue.
                try:
                    write_queue.get_nowait()
                except queue.Empty:
                    pass
        except KeyboardInterrupt:
            pass


class COMDevice(Device):
    def stream_loop(self, stop_flag, read_queue: multiprocessing.Queue, write_queue: multiprocessing.Queue):
        try:
            with serial.Serial(self.name, baudrate=115200) as ser:
                while not stop_flag.is_set():
                    # Check for incoming messages.
                    while ser.in_waiting >= MSG_SIZE:
                        # Block and read a full message.
                        in_msg = ser.read(MSG_SIZE)
                        read_queue.put(Message.deserialize(in_msg))

                    # Check for outgoing messages.
                    try:
                        out_msg = write_queue.get_nowait()
                        ser.write(out_msg.serialize())
                    except queue.Empty:
                        pass
        except KeyboardInterrupt:
            pass
