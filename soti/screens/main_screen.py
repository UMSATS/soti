"""
Main screen with on-screen messages and a command prompt.
"""

from typing import Optional
import urwid

import screens
from device import Device
from message import Message


class MainScreen(screens.Screen):
    def __init__(self, device: Optional[Device]):
        self.device = device
        self.message_widgets = urwid.SimpleFocusListWalker([])
        super().__init__()

    def on_enter(self, loop: urwid.MainLoop):
        if self.device:
            self.device.start(self._on_message_received)

    def on_exit(self, loop: urwid.MainLoop):
        if self.device:
            self.device.stop()

    def _create_root_widget(self) -> urwid.Widget:
        self.text = urwid.Text("Main Screen", align='center')
        return urwid.Filler(self.text)

    def _on_message_received(self, message: Message):
        """Called when a new message arrives."""
        self.text.set_text(str(message.as_dict()))
