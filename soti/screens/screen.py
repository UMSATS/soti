from abc import ABC, abstractmethod

import urwid

from soti_signal import Signal

class Screen(ABC):
    def __init__(self):
        self._root = self._create_root_widget()

        # Signal for switching to another screen
        self.change_screen = Signal()

    def get_root_widget(self) -> urwid.Widget:
        """Returns the screen's root widget."""
        return self._root

    @abstractmethod
    def _create_root_widget(self) -> urwid.Widget:
        """Creates the root widget of the screen."""

    def on_enter(self, loop: urwid.MainLoop) -> None:
        """Called once when entering the screen. (Can be multiple times)"""

    def on_exit(self, loop: urwid.MainLoop) -> None:
        """Called once when exiting the screen. (Can be multiple times)"""
