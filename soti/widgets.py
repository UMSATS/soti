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
        self.row_widgets = urwid.SimpleFocusListWalker([])
        super().__init__(
            urwid.Frame(
                urwid.ScrollBar(urwid.ListBox(self.row_widgets)),
                header=header_row
            )
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


class TextPrompt(urwid.WidgetWrap):
    def __init__(self, caption):
        super().__init__(
            urwid.LineBox(
                urwid.Edit(caption, wrap='clip'),
                tlcorner=urwid.LineBox.Symbols.LIGHT.TOP_LEFT_ROUNDED,
                trcorner=urwid.LineBox.Symbols.LIGHT.TOP_RIGHT_ROUNDED,
                blcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_LEFT_ROUNDED,
                brcorner=urwid.LineBox.Symbols.LIGHT.BOTTOM_RIGHT_ROUNDED
            )
        )
        self.submit = Signal()

    def selectable(self):
        return True

    def keypress(self, size, key):
        if key == 'enter':
            self.submit.emit(self._w.base_widget.get_edit_text())
            self._w.base_widget.edit_text = ""
            return None
        return super().keypress(size, key)
