"""Basic input/results Screen."""
from collections.abc import Sequence
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Dimension
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.lib.collection import Collection

TEXT_FORMAT = {"selected": "bg:#144288", "unselected": "default"}

RESULTS_DIMENSION_DICT = {
    "min": 3,
    "max": 15,
    "preferred": 10,
}
PREVIEW_DIMENSION_DICT = {
    "min": 5,
    "preferred": 15,
}


class SelectableList(FormattedTextControl):
    """Create a selectable list that is not focusable."""

    def __init__(self, focusable=False, text_format=TEXT_FORMAT, *args, **kwargs):
        self.text_format = text_format
        self._index = -1
        super().__init__(*args, **kwargs)

    @property
    def index(self):
        """Selected item index."""
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

        # update formatting for index must be included here, as text/list may have changed
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

    @property
    def selected_result(self):
        """Return the selected result."""
        if 0 <= self.index:
            return self.text[self.index][1]
        else:
            return None

class ViewScreen(object):
    """View screen with selectable results, preview."""

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
        self.results_window = Window(self.results_control, height=Dimension(**RESULTS_DIMENSION_DICT))
        self.preview_header = Window(BufferControl(focusable=False,), height=1, style="reverse")
        self.preview_window = Window(BufferControl(focusable=False),  height=Dimension(**PREVIEW_DIMENSION_DICT))
        self.status_bar = FormattedTextControl(status_bar_text)

        self.layout = Layout(
            HSplit(
                [
                    self.query_header,
                    Window(BufferControl(self.input_buffer), height=1,),
                    self.results_window,
                    self.preview_header,
                    self.preview_window,
                    Window(self.status_bar, height=1, style="reverse"),
                ]
            ),
        )

        @self.kb.add("up")
        def _(event):
            self.results_control.index -= 1
            self.update_preview()

        @self.kb.add("down")
        def _(event):
            self.results_control.index += 1
            self.update_preview()

    @property
    def input_str(self):
        return self.input_buffer.text

    @input_str.setter
    def input_str(self, text):
        return self.input_buffer.text

    def update_results(self, unused_arg=""):
        """Update self.results in-place."""
        try:
            results = self.collection.query_records(query_str=self.input_str)
        except Exception:
            self.status_bar.text = "(invalid query)"
        else:
            results = sorted(results, key=lambda x: x[1])
            self.results_control.text = results
            self.results_control.index = 0
            self.update_preview()

    def update_status_text(self, text):
        """Update the status bar text."""
        pass

    def update_header_text(self, text):
        """Update the header text."""
        pass

    def update_preview(self):
        """Update preview window text."""

        if isinstance(self.results_control.selected_result, str):
            document_id = self.results_control.selected_result.split("\n")[0]
            record = self.collection.return_record(document_id)
            preview = record["document_type"].preview(record)
        else:
            preview = "(no preview)"
        self.preview_window.content.buffer.text = preview

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

    window = ViewScreen(state=state)

    @window.kb.add("c-c")
    def _(event):
        event.app.exit()

    application = Application(
        layout=window.layout, key_bindings=window.kb, full_screen=True
    )
    with patch_stdout():
        application.run()
