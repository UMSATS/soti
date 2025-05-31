"""
Main script and entry point of the application. This is where global state is
managed.
"""

import urwid

import config
from screens.main_screen import MainScreen
from screens.device_selector import DeviceSelector
from device import Device


class App():
    """Represents the entire SOTI application."""

    def __init__(self):
        # Define the main loop which will get executed in the run() method.
        self.loop = urwid.MainLoop(
            urwid.SolidFill(" "), # placeholder - will get swapped
            config.PALETTE,
            unhandled_input=self.unhandled_input
        )

        self.current_screen = None

        # Switch to the starting screen of the application.
        initial_screen = DeviceSelector()
        initial_screen.finished.connect(self._on_device_selector_finished)
        self.change_screen(initial_screen)

    def run(self):
        try:
            self.loop.run()
        finally:
            self.current_screen.on_exit(self.loop)

    def unhandled_input(self, key):
        """
        Handles user input not captured by widgets in the tree. This is where
        global key bindings should be implemented.
        """
        if key == 'q':
            raise urwid.ExitMainLoop()

    def change_screen(self, screen):
        """Switches to a different screen and swaps the UI."""
        if self.current_screen is not None:
            self.current_screen.on_exit(self.loop)
        self.current_screen = screen
        screen.on_enter(self.loop)
        self.loop.widget = screen.get_top_level_widget()

    def _on_device_selector_finished(self, selected_device: Device):
        if selected_device is not None:
            main_screen = MainScreen(selected_device)
            self.change_screen(main_screen)


if __name__ == "__main__":
    App().run()
