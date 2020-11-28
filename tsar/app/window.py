"""
Basic input/results Screen.
"""
from collections.abc import Sequence
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Dimension
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import TabsProcessor
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.widgets import HorizontalLine
from tsar.lib.collection import Collection, DOCTYPES
from tsar.lib.services import TaskManager
from tsar.config import SEARCH_RECORD_COLORS, DEFAULT_COLLECTION
from tsar import tasks
from tsar.tasks import DEFAULT_HOUR, DEFAULT_MINUTE, DEFAULT_SECONDS
from datetime import datetime
from operator import itemgetter

TEXT_FORMAT = {"selected": "bg:#144288", "unselected": "default"}


RESULTS_DIMENSION_DICT = {
    "min": 2,
    "max": 15,
    "preferred": 10,
}
PREVIEW_DIMENSION_DICT = {
    "min": 6,
    "preferred": 15,
}


class SelectableList(FormattedTextControl):
    """Create a selectable list that is not focusable.
    Text property must be set as list of strings; outputs formatted list of strings
    """

    def __init__(self, focusable=False, text_format=TEXT_FORMAT, *args, **kwargs):
        self.text_format = text_format
        self._index = 0
        super().__init__(*args, **kwargs)

    @property
    def index(self):
        """Define a "selected item" index for self.text."""
        return self._index

    @index.setter
    def index(self, value):
        """Selected result index."""
        idx_init = self._index
        idx_max = len(self.text) - 1

        if isinstance(self.text, str):
            self._index = -1
            return
        elif isinstance(self.text, Sequence):
            # self.text is list-like; set within index bounds:
            if 0 <= value <= idx_max:
                self._index = value
            elif value < 0:
                self._index = 0
            elif idx_max < value:
                self._index = idx_max

        # update formatting for index; text may have changed
        if 0 <= idx_init <= len(self.text) - 1:
            _, res_init = self.text[idx_init]
            self._text[idx_init] = (self.text_format["unselected"], res_init)
        _, res = self.text[self.index]
        self._text[self.index] = (self.text_format["selected"], res)

    @property
    def text(self):
        """Return formatted results, with highlighted item at self.index."""
        return self._text

    @text.setter
    def text(self, value):
        if len(value) == 0:
            formatted_results = "(no results)"
        # text is list
        elif isinstance(value, Sequence):
            formatted_results = [
                (self.text_format["unselected"], f"{res}\n") for res in value
            ]
        self._text = formatted_results


class ViewScreen1(object):
    """View screen format 1: buffer, results, preview."""

    def __init__(
        self, state, header_text="(header text)", status_bar_text="(status bar text)"
    ):
        self.state = state
        self.collection = self.state["active_collection"]
        self.kb = KeyBindings()

        # layout components
        self.query_header = Window(
            FormattedTextControl(header_text), height=1, style="reverse",
        )
        self.input_buffer = Buffer(multiline=False)
        self.input_buffer.on_text_changed += self.update_results
        self.results_control = SelectableList(text="")
        self.preview_control = BufferControl(focusable=False,)
        self.status_bar = FormattedTextControl(status_bar_text)

        self.layout = Layout(
            HSplit(
                [
                    self.query_header,
                    Window(BufferControl(self.input_buffer), height=1,),
                    Window(self.results_control),
                    Window(self.preview_control),
                    Window(self.status_bar, height=1, style="reverse"),
                ]
            ),
        )

        @self.kb.add("up")
        def _(event):
            self.results_control.index -= 1

        @self.kb.add("down")
        def _(event):
            self.results_control.index += 1

    @property
    def input_str(self):
        return self.input_buffer.text

    def update_results(self, unused_arg=""):
        """Update self.results in-place."""
        try:
            results = self.collection.query_records(query_str=self.input_str)
        except Exception:
            self.results = []
            self.status_bar.text = "(invalid query)"
        else:
            results = sorted(results, key=lambda x: x[1])
            self.results_control.text = results
            self.results_control.index = 0
            self.status_bar.text = ""

        # self.preview_control.text = self.results_control.index


if __name__ == "__main__":
    """stand-alone window test."""

    coll_ids = Collection.registered_collections()
    collections = [Collection.load(coll) for coll in coll_ids]
    coll = collections[0]

    state = {
        "active_collection": coll,
        "collections": {
            coll: {"current_doc": None, "query_str": "", "current_results": [],},
        },
    }

    window = ViewScreen1(state=state)

    @window.kb.add("c-c")
    def _(event):
        event.app.exit()

    application = Application(
        layout=window.layout, key_bindings=window.kb, full_screen=True
    )
    with patch_stdout():
        application.run()
