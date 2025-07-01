"""
Entry point of the application. This is where all global state is managed.
"""

import urwid

import config
import screens


class App():
    """Represents the entire SOTI application."""

    def __init__(self):
        # This loop will take control of the main thread in run().
        self.loop = urwid.MainLoop(
            urwid.SolidFill(" "), # placeholder - will get swapped
            config.PALETTE,
            unhandled_input=self.unhandled_input
        )

        # The current active screen.
        self.current_screen: screens.Screen | None = None

        # Switch to the initial screen of the application.
        self.change_screen(screens.DeviceSelector())

    def run(self):
        try:
            self.loop.run()
        finally:
            self.current_screen.on_exit(self.loop)

    def change_screen(self, screen: screens.Screen):
        """Switches to another screen and swaps the UI."""
        if self.current_screen is not None:
            self.current_screen.on_exit(self.loop)

        self.current_screen = screen

        screen.change_screen.connect(self.change_screen)
        self.loop.widget = screen.get_root_widget()
        screen.on_enter(self.loop)

    def unhandled_input(self, key):
        """
        Handles user input not captured by widgets in the tree. This is where
        global key bindings should be implemented.
        """
        if key == 'q':
            raise urwid.ExitMainLoop()


if __name__ == "__main__":
    App().run()
