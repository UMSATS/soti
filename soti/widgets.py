import urwid

from soti_signal import Signal

class IconButton(urwid.WidgetWrap):
    def __init__(self, icon: str, label: str):
        text = [f" {icon} ", label]
        super().__init__(
            urwid.AttrMap(urwid.Text(text), 'button', 'button focus')
        )
        self.clicked = Signal()

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == 'enter':
            self.clicked.emit()
            return None
        return super().keypress(size, key)
