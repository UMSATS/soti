"""
Collection of re-useable widgets created for the SOTI TUI.
"""

from typing import Literal
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


class TableWidget(urwid.WidgetWrap):
    def __init__(self, columns: list[tuple[str, int | Literal['expand']]]):
        self._columns = columns
        header_row = self._create_row([c[0] for c in columns], 'table header')
        self.row_widgets = urwid.SimpleFocusListWalker([header_row])
        super().__init__(
            urwid.ListBox(self.row_widgets)
        )

    def add_row(self, kv_pairs: dict):
        row_contents = []
        for name, _ in self._columns:
            row_contents.append(kv_pairs.get(name, "---"))
        row = self._create_row(row_contents, 'table cell')
        self.row_widgets.append(row)

    def _create_row(self, contents: list[str], style: str) -> urwid.Widget:
        widgets = []
        for (_, width), content in zip(self._columns, contents):
            widget = urwid.AttrMap(urwid.Text(content, wrap='ellipsis'), style)
            if width != 'expand':
                widget = (width, widget)
            widgets.append(widget)
        row = urwid.Columns(widgets, dividechars=1)
        return row
