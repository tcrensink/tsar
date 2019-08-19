#!/usr/bin/env python
"""
separate focus and cursor.

- cursor remains in top window
- up/down arrows change focus in separate window
"""
from __future__ import unicode_literals

from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    HSplit,
    VerticalAlign,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import D
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import Frame
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit import print_formatted_text
from string import printable

TITLE = HTML(""" <u>VSplit VerticalAlign</u> example.
 Press <b>'q'</b> to quit.""")

STYLE = {
    'selected': 'bg:#944288',
    'unselected': 'default'
}

RESULTS_LIST = ['line {}'.format(j) for j in range(15)]

RESULT_TEXT = """
In this example:

1 The cursor remains in the top window, ready for reading text input, even as the selected row changes
2 up/down arrows change the selected row (manually done by changing the text style from a key binding)
3 An additional callback is mapped to the row number, changing this text

This is very similar to the prompt completion, but the output is not an auto-completion of the input text
"""

def return_preview(n, p=3):
    """return some gibberish result based on the focus position
    """
    N = len(printable)

    cond = lambda x: x == '\n'

    try:
        preview = ''.join([printable[(printable.index(c) + n*p)%N] if not cond(c) else c for c in RESULT_TEXT])
    except TypeError:
        preview = "(None)"
    return preview


class LineFocus(object):
    """spoof a "focus" in the list of results, separated from a cursor
    """
    def __init__(self, results_list=None, style=STYLE, index=0):

        self.style = style
        if results_list is None:
            results_list = []
        self.results = self.apply_default_format(results_list)
        # self._index = index
        self.index = index

    @property
    def result_styles(self):
        _result_styles, _ = zip(*self.results)
        return list(_result_styles)

    @property
    def result_texts(self):
        _, _result_texts = zip(*self.results)
        return list(_result_texts)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        """change the results `style` based active_result_index
        """
        # self._index may not exist:
        try:
            old_index = self._index
        except AttributeError:
            old_index = None

        # correct value bounds:
        try:
            if new_index >= len(self.results):
                new_index = len(self.results) - 1
            elif new_index < 0:
                new_index = 0
        except TypeError:
            pass
        self._index = new_index
        self._update_selected(old_index, new_index)

    def _update_selected(self, old_index, new_index):
        """change the style of previous index to default, new index to selected
        Either old or new index may be None and should be handled separately
        """

        try:
            _, res = self.results[old_index]
            self.results[old_index] = (self.style["unselected"], res)
        except TypeError:
            pass
        try:
            _, res = self.results[new_index]
            self.results[new_index] = (self.style["selected"], res)
        except TypeError:
            pass

    def apply_default_format(self, results_list):
        """convert a list of result strings to a FormattedText object

        print formatted results using print_formatted_text
        """
        results_list = ["{}\n".format(res) for res in results_list]
        line_focus = FormattedText([(self.style['unselected'], res) for res in results_list])
        return line_focus


query_window = Window(
    BufferControl(
        Buffer(
            name='query_buffer',
            multiline=False
        )
    ),
    height=1,
)


line_focus = LineFocus(RESULTS_LIST)
result_window = Window(
    FormattedTextControl(line_focus.results),
    height=len(line_focus.results)
)


preview_window = Window(
    FormattedTextControl(return_preview(line_focus.index)),
    height=20
)

body = HSplit(
    [
        query_window,
        result_window,
        preview_window
    ],
    padding=1, padding_style='bg:default', align=VerticalAlign.TOP, padding_char='_'
)


# 2. Key bindings
kb = KeyBindings()

@kb.add('q')
def _(event):
    " Quit application. "
    event.app.exit()

# select result:
@kb.add('up')
@kb.add('down')
def _(event):
    """change selection based on key presses
    - update selected result (line_focus.index)
    - update preview
    """
    key = event.key_sequence[0].key
    try:
        if key == 'up':
            line_focus.index -= 1
        if key == 'down':
            line_focus.index += 1
    except TypeError:
        line_focus.index = 0
    preview_window.content.text = return_preview(line_focus.index)


# 3. The `Application`
application = Application(
    layout=Layout(body),
    key_bindings=kb,
    full_screen=True)


def run():
    application.run()


if __name__ == '__main__':
    run()
