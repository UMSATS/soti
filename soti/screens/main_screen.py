import multiprocessing
import queue

import urwid

from device import Device
from message import Message


class MainScreen():
    def __init__(self, device: Device):
        self.text = urwid.Text("Main Screen", align='center')
        self.widget = self._create_widget()
        self.device = device
        self.read_queue = None
        self.write_queue = None
        self.stop_flag = None
        self.device_process = None
        self.update_alarm = None

    def get_top_level_widget(self) -> urwid.Widget:
        return self.widget

    def on_enter(self, loop: urwid.MainLoop):
        """Called once when entering the screen. (Can be multiple times)"""
        # Spawn a new process to transfer data.
        self.read_queue = multiprocessing.Queue()
        self.write_queue = multiprocessing.Queue()
        self.stop_flag = multiprocessing.Event()
        self.device_process = multiprocessing.Process(
            target=self.device.stream_loop,
            args=(self.stop_flag, self.read_queue, self.write_queue),
            daemon=True
        )
        self.device_process.start()

        # Schedule the first update.
        self.update_alarm = loop.set_alarm_in(0.1, self._update)

    def on_exit(self, loop: urwid.MainLoop):
        """Called once when exiting the screen. (Can be multiple times)"""
        # Remove the update alarm.
        loop.remove_alarm(self.update_alarm)

        # Terminate the process.
        self.stop_flag.set()
        self.device_process.join()

    def _update(self, loop: urwid.MainLoop, user_data):
        try:
            msg = self.read_queue.get_nowait()
            self._on_message_received(msg)
        except queue.Empty:
            pass

        # Schedule the next update.
        loop.set_alarm_in(0.1, self._update)

    def _on_message_received(self, message: Message):
        """
        Called when a new message arrives.
        """
        self.text.set_text(str(message.as_dict()))

    def _create_widget(self) -> urwid.Widget:
        """Creates the top-level widget of the screen. Called once in __init__."""
        return urwid.Filler(self.text)
