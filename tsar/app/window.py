"""Basic input/results Screen."""
from collections.abc import Sequence
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout import Dimension
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.processors import TabsProcessor
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.lib.collection import Collection

TEXT_FORMAT = {"selected": "bg:#144288", "unselected": "default"}

RESULTS_DIMENSION_DICT = {
    "min": 3,
    "max": 20,
    "preferred": 14,
}
PREVIEW_DIMENSION_DICT = {
    "min": 5,
    "preferred": 12,
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
            return self.text[self.index][1].strip()
        else:
            return None

    def index_of_result(self, result):
        """Given a result, return its index, else None."""
        results = {res[1].strip(): j for j, res in enumerate(self.text)}
        if self.selected_result in results.keys():
            idx = results[self.selected_result]
        else:
            idx = None
        return idx

class ViewScreen(object):
    """View screen with selectable results, preview."""

    def __init__(self, state,):
        self.state = state
        self.kb = KeyBindings()

        # layout components
        self.header_bar = FormattedTextControl(focusable=False,)
        self.input_buffer = Buffer(multiline=False)
        self.input_buffer.on_text_changed += self.update_results
        self.results_control = SelectableList(text="")
        self.preview_bar = FormattedTextControl(focusable=False,)
        self.preview_buffer = BufferControl(focusable=False, input_processors=[TabsProcessor(tabstop=4, char1=" ", char2=" ")],)
        self.status_bar = FormattedTextControl()

        self.layout = Layout(
            HSplit(
                [
                    Window(self.header_bar, height=1, style="reverse"),
                    Window(BufferControl(self.input_buffer), height=1,),
                    Window(self.results_control, height=Dimension(**RESULTS_DIMENSION_DICT)),
                    Window(self.preview_bar, height=1, style="reverse"),
                    Window(self.preview_buffer, wrap_lines=True, height=Dimension(**PREVIEW_DIMENSION_DICT)),
                    Window(self.status_bar, height=1, style="reverse"),
                ]
            ),
        )
        self.reset_view()

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
        self.input_buffer.text = text

    def update_results(self, unused_arg=""):
        """Update self.results in-place."""
        try:
            results = self.state["active_collection"].query_records(query_str=self.input_str)
        except Exception:
            self.results_control.text = ["(invalid query)"]
        else:
            results = sorted(results, key=lambda x: x[1])
            self.results_control.text = results
            self.results_control.index = 0
        self.update_preview()

    def update_header_bar(self, text=None):
        """Update the header text."""
        if text is None:
            coll = self.state["active_collection"]

            fields = set()
            for index in coll.search_indices:
                index_fields = coll.client.return_fields(index)
                fields.update(index_fields.keys())
            text = f"search: {' | '.join(sorted(fields))}"
        self.header_bar.text = text

    def update_status_bar(self, text=None):
        """Update the status bar text."""
        coll = self.state["active_collection"]
        df = coll.records_db.df
        _doc_count = df.document_type.value_counts().reset_index(name="counts")
        doc_count_str = ", ".join([f"{row[1]} {row[0].__name__}" for row in _doc_count.values])
        if text is None:
            text = (
                f'{coll.records_db.df.shape[0]} docs in '
                f'"{coll.collection_id}": '
                f'{doc_count_str}'
            )
        self.status_bar.text = text

    def update_preview_bar(self, text=None):
        """Update the preview bar text."""
        coll = self.state["active_collection"]
        if text is None:
            text = "preview"
        self.preview_bar.text = text

    def update_preview(self):
        """Update preview window text."""
        if isinstance(self.results_control.selected_result, str):
            document_id = self.results_control.selected_result.split("\n")[0]
            record = self.state["active_collection"].return_record(document_id)
            if record:
                preview = record["document_type"].preview(record)
            else:
                preview = "(no preview available)"
        else:
            preview = "(no preview available)"
        self.preview_buffer.buffer.text = preview

    def reset_view(self):
        """Update all values from shared state dict."""
        self.update_header_bar()
        self.update_preview_bar()
        self.update_preview()
        self.update_status_bar()


if __name__ == "__main__":
    """stand-alone window test."""

    coll_ids = Collection.registered_collections()
    collections = [Collection.load(coll) for coll in coll_ids]
    window = ViewScreen(state={"active_collection": collections[0]})
    @window.kb.add("c-c")
    def _(event):
        event.app.exit()
    with patch_stdout():
        Application(
            layout=window.layout, key_bindings=window.kb, full_screen=True
        ).run()
