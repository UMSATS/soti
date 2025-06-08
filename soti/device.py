import multiprocessing
import serial
import queue
from abc import ABC, abstractmethod
from typing import Callable, Optional

from message import Message, MSG_SIZE


class Device(ABC):
    def __init__(self):
        self._process: Optional[multiprocessing.Process] = None
        self._read_queue = multiprocessing.Queue()
        self._write_queue = multiprocessing.Queue()
        self._callback: Optional[Callable[[Message], None]] = None

    def start(self, message_callback: Optional[Callable[[Message], None]] = None):
        """Spawns a separate process to read and write messages from queues."""
        self._callback = message_callback
        if self._process and self._process.is_alive():
            return  # Already running
        self._process = multiprocessing.Process(target=self._run)
        self._process.start()

    def stop(self):
        """Stops the process. The device can be re-started with the start() method."""
        if self._process:
            self._write_queue.put(None)  # Sentinel value to terminate
            self._process.join()
            self._process = None

    def write(self, message: Message):
        """Enqueues a message for transmission in the subprocess."""
        self._write_queue.put(message)

    def read(self) -> Message:
        """Reads a message from the read queue, if there is one. Otherwise throws queue.Empty."""
        return self._read_queue.get_nowait()

    @abstractmethod
    def _run(self):
        """Override this method to implement specific device behavior."""
        pass


class SerialDevice(Device):
    def __init__(self,  port: str, baudrate: int = 115200):
        super().__init__()
        self.port = port
        self.baudrate = baudrate

    def _run(self):
        try:
            ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
        except serial.SerialException as e:
            print(f"[SerialDevice: {self.port}] Failed to open serial port: {e}")
            return

        while True:
            try:
                msg = self._write_queue.get_nowait()
                if msg is None: # Check for termination sentinel
                    break  # Exit process
                ser.write(msg.serialize())
            except queue.Empty:
                pass

            # Read if bytes are available
            if ser.in_waiting >= MSG_SIZE:
                data = ser.read(MSG_SIZE)
                try:
                    msg = Message.deserialize(data)
                    if self._callback:
                        self._callback(msg)
                except Exception as e:
                    print(f"[SerialDevice: {self.port}] Deserialization error: {e}")

        ser.close()


class VirtualDevice(Device):
    def _run(self):
        while True:
            try:
                msg = self._write_queue.get_nowait()
                if msg is None: # Check for termination sentinel
                    break  # Exit process
            except queue.Empty:
                pass
            # Don't read any messages
