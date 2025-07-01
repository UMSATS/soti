"""
The screen where the target input device is selected.
"""

from typing import Optional

import urwid
import serial.tools.list_ports

import config
import screens
from device import Device, SerialDevice
from utils.constants import RES_DIR
from widgets import IconButton


class DeviceOption:
    def __init__(self, name: str, description: str, device: Optional[Device], icon: str = config.ICONS['PORT_DEFAULT']):
        self.name = name
        self.description = description
        self.device = device
        self.icon = icon


class DeviceSelector(screens.Screen):
    def __init__(self):
        # List of widgets for the menu items
        self.menu_items = urwid.SimpleFocusListWalker([])
        super().__init__()

    def on_enter(self, loop: urwid.MainLoop):
        self._refresh_menu_items()

    def _create_root_widget(self) -> urwid.Widget:
        with open(RES_DIR / "banner.txt", 'r', encoding='utf-8') as file:
            banner_art = file.read()

        # Create the banner and title.
        banner = urwid.Text(('soti banner', banner_art), align='center')
        title = urwid.Text(('soti title', "Satellite • Operations • Testing • Interface\n\n"), align='center')

        # Create menu of serial devices
        menu = urwid.Padding(urwid.LineBox(
            urwid.ListBox(self.menu_items),
            title="Select Input Device",
            title_attr='title',
            title_align='center',
            tlcorner=urwid.LineBox.Symbols.LIGHT.TOP_LEFT_ROUNDED,
            trcorner=urwid.LineBox.Symbols.LIGHT.TOP_RIGHT_ROUNDED,
            blcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_LEFT_ROUNDED,
            brcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_RIGHT_ROUNDED
        ), width=70, align='center')

        # Create footer with keyboard shortcuts
        footer_text = [
            ('accent', "q"), " to quit  ",
            ('accent', "↑↓"), " to navigate  ",
            ('accent', "Enter"), " to select"
        ]
        footer = urwid.Text(footer_text, align='center')
        
        # Add version info
        version = urwid.Text(('info', f"SOTI v{config.APP_VERSION} - © 2025 UMSATS"), align='right')
        
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

    def _get_device_options(self) -> list[DeviceOption]:
        """Returns a list of available devices as DeviceOption objects."""
        devices: list[DeviceOption] = []

        # Read available COM devices with the serial module.
        for comport in serial.tools.list_ports.comports():
            device = SerialDevice(comport.device)
            devices.append(DeviceOption(comport.device, comport.description, device))

        # Add the "No Device" option.
        no_device = DeviceOption(
            "No Device",
            "Proceed without connecting to a device.",
            device=None,
            icon=config.ICONS['PORT_NONE']
        )
        devices.append(no_device)

        return devices

    def _refresh_menu_items(self):
        """Updates the list of devices."""
        self.menu_items.clear()
        for opt in self._get_device_options():
            w = IconButton(opt.icon, opt.name + " - " + opt.description)
            w.clicked.connect(self._on_device_selected, args=(opt.device,))
            self.menu_items.append(w)

    def _on_device_selected(self, device: Optional[Device]):
        """Called when a device is selected by the user."""
        next_screen = screens.MainScreen(device)
        self.change_screen.emit(next_screen)
