"""Represents the screen where the target device is selected."""

import urwid
import serial.tools.list_ports

import config
from device import COMDevice, Device
from widgets import IconButton
from soti_signal import Signal


class DeviceSelector():
    def __init__(self):
        # Create an empty list of menu items.
        self.menu_items = urwid.SimpleFocusListWalker([])

        # Create the top-level widget for the screen.
        self.widget = self._create_widget(self.menu_items)

        # "Finished" signal to exit the screen with some result.
        self.finished = Signal()

    def get_top_level_widget(self) -> urwid.Widget:
        return self.widget

    def on_enter(self, loop: urwid.MainLoop):
        """Called once when entering the screen. (Can be called many times)"""
        self._refresh_menu_items()

    def on_exit(self, loop: urwid.MainLoop):
        """Called once when exiting the screen. (Can be called many times)"""

    def _create_widget(self, menu_items: urwid.SimpleFocusListWalker) -> urwid.Widget:
        """Creates the top-level widget of the screen. Called once in __init__."""
        # Create the banner and title.
        banner = urwid.Text(('soti banner', "[ Banner Art ]"), align='center')
        title = urwid.Text(('soti title', "Satellite • Operations • Testing • Interface\n\n"), align='center')

        # Create menu of serial devices
        menu = urwid.Padding(urwid.LineBox(
            urwid.ListBox(menu_items),
            title=" Select Input Device ",
            title_attr='title',
            title_align='center',
            tline="═",
            bline="═",
            lline="│",
            rline="│",
            tlcorner="╒",
            trcorner="╕",
            blcorner="╘",
            brcorner="╛"
        ), width=70, align='center')

        # Create footer with keyboard shortcuts
        footer_text = [
            ('accent', "q"), " to quit  ",
            ('accent', "↑↓"), " to navigate  ",
            ('accent', "Enter"), " to select"
        ]
        footer = urwid.Text(footer_text, align='center')
        
        # Add version info
        version = urwid.Text(('info', "SOTI v2.0 - © 2025 UMSATS"), align='right')
        
        # Combine all elements
        pile = urwid.Pile([
            ('weight', 1, urwid.Filler(urwid.Divider())),
            ('pack', banner),
            ('pack', title),
            ('fixed', 7, menu),
            ('weight', 1, urwid.Filler(urwid.Divider())),
            ('pack', footer),
            ('pack', version)
        ])
        
        # Apply padding around everything
        return urwid.Padding(pile, left=3, right=3)

    def _get_available_devices(self) -> list[Device]:
        """Returns all available devices as Device objects."""
        devices: list[Device] = []

        # Read available COM devices with the serial module.
        for com_port in serial.tools.list_ports.comports():
            devices.append(COMDevice(com_port.device, com_port.description))

        # Add the special virtual device.
        virtual_device = Device(
            "Virtual Mode",
            "For off-board testing.",
            icon=config.ICONS['PORT_VIRTUAL']
        )
        devices.append(virtual_device)

        return devices

    def _refresh_menu_items(self):
        """Updates the list of devices."""
        self.menu_items.clear()
        for p in self._get_available_devices():
            w = IconButton(p.icon, p.name + " - " + p.description)
            w.clicked.connect(self._on_device_selected, args=(p,))
            self.menu_items.append(w)

    def _on_device_selected(self, device: Device):
        """Called when a device is selected by the user."""
        self.finished.emit(device)
