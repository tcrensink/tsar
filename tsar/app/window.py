"""
Basic Screen interface.
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
    """Create a selectable list that does take the cursor."""

    def __init__(self, focusable=False, text_format=TEXT_FORMAT, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_format = text_format
        self._index = 0

    @property
    def index(self):
        """Define a "selected item" index if self.text is list-like."""
        return self._index

    @index.setter
    def index(self, value):
        """Selected result index."""
        if isinstance(self.text, str):
            self._index = 0
        elif isinstance(self.text, Sequence):
            # self.text is list-like; set within index bounds:
            lmax = len(self.text) - 1
            if 0 <= value <= lmax:
                self._index = value
            elif value < 0:
                self._index = 0
            elif lmax < value:
                self._index = lmax

    @property
    def text(self):
        """Return formatted results, with highlighted item at self.index."""
        if len(self._text) == 0:
            formatted_results = [(self.text_format["unselected"], "(no results)")]

        elif isinstance(self._text, str):
            formatted_results = [
                (self.text_format["unselected"], f"{res}\n")
                for res in self._text.split("\n")
            ]
            _, res = formatted_results[self.index]
            formatted_results[self.index] = (self.text_format["selected"], res)

        elif isinstance(self._text, Sequence) and isinstance(self._text[0], str):
            formatted_results = [
                (self.text_format["unselected"], f"{res}") for res in self._text
            ]
            _, res = formatted_results[self.index]
            formatted_results[self.index] = (self.text_format["selected"], res)

        elif isinstance(self._text, Sequence) and isinstance(self._text[0], tuple):
            formatted_results = [
                (self.text_format["unselected"], f"{res[1]}") for res in self._text
            ]
            _, res = formatted_results[self.index]
            formatted_results[self.index] = (self.text_format["selected"], res)

        return formatted_results

    @text.setter
    def text(self, value):
        self._text = value


class ViewScreen1(object):
    """View screen format 1: buffer, results, preview."""

    def __init__(
        self, state,
    ):
        self.state = state
        self.collection = self.state["active_collection"]
        self.kb = KeyBindings()

        # layout components
        self.query_header = Window(
            FormattedTextControl("example text"), height=1, style="reverse",
        )
        self.input_buffer = Buffer(multiline=False)
        self.input_buffer.on_text_changed += self.update_results

        self.results_control = SelectableList(text="")
        # self.results_control.text = self.results_control.results
        self.layout = Layout(
            HSplit(
                [
                    self.query_header,
                    Window(BufferControl(self.input_buffer), height=1,),
                    Window(self.results_control),
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

    @input_str.setter
    def input_str(self, new_input_str):
        self.query_buffer.text = new_input_str

    def update_results(self, unused_arg=""):
        """Update self.results in-place."""
        try:
            results = self.collection.query_records(query_str=self.input_str)
        except Exception:
            self.results = []
            self.status_textcontrol.text = "(invalid query)"
        else:
            results = sorted(results, key=lambda x: x[1])
            formatted_results = [
                (TEXT_FORMAT["unselected"], f"{res}\n") for res in results
            ]
            self.results_control.text = formatted_results


if __name__ == "__main__":
    """stand-alone version of the search window for debugging."""

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
    application.run()
