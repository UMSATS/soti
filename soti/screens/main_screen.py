"""
Main screen with on-screen messages and a command prompt.
"""

from typing import Optional
import queue

import urwid

import screens
from device import Device
from message import Message
from widgets import TableWidget
from session_logger import parse_msg_body


class MainScreen(screens.Screen):
    def __init__(self, device: Optional[Device]):
        self.device = device
        self.message_widgets = urwid.SimpleFocusListWalker([])
        self.msg_id = 0
        self.update_alarm = -1
        super().__init__()

    def on_enter(self, loop: urwid.MainLoop):
        if self.device:
            self.device.start()
            self.update_alarm = loop.set_alarm_in(0.1, self._update)

    def on_exit(self, loop: urwid.MainLoop):
        if self.device:
            self.device.stop()
            loop.remove_alarm(self.update_alarm)

    def _create_root_widget(self) -> urwid.Widget:
        self.table = TableWidget(columns=[
            ("ID", 3),
            ("Timestamp", 9),
            ("Transaction", 'expand'),
            ("Pri", 3),
            ("Arguments", 'expand')
        ])
        return urwid.Padding(self.table, left=1, right=1)

    def _update(self, loop: urwid.MainLoop, user_data):
        try:
            while True:
                msg = self.device.read()
                self._on_message_received(msg)
        except queue.Empty:
            pass

        self.update_alarm = loop.set_alarm_in(0.1, self._update)

    def _on_message_received(self, msg: Message):
        """Called when a new message arrives."""
        transaction = f"{str(msg.sender.name)} → {str(msg.recipient.name)} : {str(msg.cmd_id.name)}"
        body_contents = parse_msg_body(msg.cmd_id, msg.body)
        arguments = ""
        for key, value in body_contents.items():
            arguments += f"{key}={value}, "
        self.table.add_row({
            'ID': str(self.msg_id),
            'Timestamp': str(msg.time),
            'Transaction': transaction,
            'Pri': str(msg.priority),
            'Arguments': arguments
        })
        self.msg_id += 1
