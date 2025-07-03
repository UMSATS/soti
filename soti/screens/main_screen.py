"""
Main screen with on-screen messages and a command prompt.
"""

import datetime
import queue

import urwid

import screens
from device import Device
from message import Message
from utils.constants import NodeID
from widgets import Console, TableWidget
from session_logger import parse_msg_body
import parser


COMMAND_LIST = ["send"]

INTRO_TEXT = """Welcome to the SOTI CLI!

Send messages with:
send <Command Name> [Message Data] [Options]

"""

class MainScreen(screens.Screen):
    def __init__(self, device: Device):
        self.device = device
        self.message_widgets = urwid.SimpleFocusListWalker([])
        self.msg_id = 0
        self.sender_id = NodeID.CDH
        self.update_alarm = -1
        super().__init__()

    def on_enter(self, loop: urwid.MainLoop):
        self.device.start()
        self.update_alarm = loop.set_alarm_in(0.1, self._update)

    def on_exit(self, loop: urwid.MainLoop):
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

        self.console = Console(('cli prompt prefix', " >> "), output=INTRO_TEXT)
        self.console.submit.connect(self._on_command_entered)

        top_panel = urwid.LineBox(
            self.table,
            title="Bus Traffic",
            title_align='left',
            title_attr='title',
            tlcorner=urwid.LineBox.Symbols.LIGHT.TOP_LEFT_ROUNDED,
            trcorner=urwid.LineBox.Symbols.LIGHT.TOP_RIGHT_ROUNDED,
            blcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_LEFT_ROUNDED,
            brcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_RIGHT_ROUNDED
        )

        bottom_panel = urwid.LineBox(
            self.console,
            title="CLI",
            title_align='left',
            title_attr='title',
            tlcorner=urwid.LineBox.Symbols.LIGHT.TOP_LEFT_ROUNDED,
            trcorner=urwid.LineBox.Symbols.LIGHT.TOP_RIGHT_ROUNDED,
            blcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_LEFT_ROUNDED,
            brcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_RIGHT_ROUNDED
        )

        command_list_markup = ["Commands: "]
        for i, cmd in enumerate(COMMAND_LIST):
            command_list_markup.append(('accent', cmd))
            if i < len(COMMAND_LIST)-1:
                command_list_markup.append(", ")

        bottom_ribbon = urwid.Columns([
            ('pack', urwid.Text(command_list_markup, wrap='clip')),
            urwid.Text(["Quit: ", ('accent', "q"), " or ", ('accent', "Ctrl+C")], wrap='clip'),
            ('pack', urwid.Text("(c) 2025 UMSATS", align='right', wrap='clip'))
        ], dividechars=8)

        return urwid.Pile([
            ('weight', 2, top_panel),
            ('weight', 1, bottom_panel),
            ('pack', bottom_ribbon)
        ])

    def _update(self, loop: urwid.MainLoop, user_data):
        try:
            while True:
                msg = self.device.read()
                self._on_message_received(msg)
        except queue.Empty:
            pass

        self.update_alarm = loop.set_alarm_in(0.1, self._update)

    def _on_command_entered(self, text: str):
        parts = text.split()
        args = " ".join(parts[1:])

        match parts[0]:
            case "send":
                try:
                    msg = parser.parse_send(args, self.sender_id)
                    self.device.write(msg)
                except (ValueError, parser.ArgumentException) as e:
                    self.console.print(str(e))
                    return

    def _on_message_received(self, msg: Message):
        """Called when a new message arrives."""
        transaction = f"{str(msg.sender.name)} → {str(msg.recipient.name)} : {str(msg.cmd.name)}"
        body_contents = parse_msg_body(msg.cmd, msg.body)
        arguments = ""
        for key, value in body_contents.items():
            arguments += f"{key}={value}, "
        self.table.add_row({
            'ID': str(self.msg_id),
            'Timestamp': str(datetime.datetime.now().strftime("%T")),
            'Transaction': transaction,
            'Pri': str(msg.priority),
            'Arguments': arguments
        })
        self.msg_id += 1
