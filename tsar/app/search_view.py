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
from tsar.app.layout_components import SelectableList

TEXT_FORMAT = {"selected": "bg:#144288", "unselected": "default"}

RESULTS_DIMENSION_DICT = {
    "min": 3,
    "max": 20,
    "preferred": 12,
}
PREVIEW_DIMENSION_DICT = {
    "min": 5,
    "preferred": 14,
}


class SearchView(object):
    """View screen with selectable results, preview."""

    def __init__(
        self, state,
    ):
        self.state = state
        self.kb = KeyBindings()

        # layout components
        self.header_bar = FormattedTextControl(focusable=False,)
        self.input_buffer = Buffer(multiline=False)
        self.input_buffer.on_text_changed += self.update_results
        self.results_control = SelectableList(text="")
        self.preview_bar = FormattedTextControl(focusable=False,)
        self.preview_buffer = BufferControl(focusable=False,)
        self.status_bar = FormattedTextControl()

        self.layout = Layout(
            HSplit(
                [
                    Window(self.header_bar, height=1, style="reverse"),
                    Window(BufferControl(self.input_buffer), height=1,),
                    Window(
                        self.results_control, height=Dimension(**RESULTS_DIMENSION_DICT)
                    ),
                    Window(self.preview_bar, height=1, style="reverse"),
                    Window(
                        self.preview_buffer,
                        wrap_lines=True,
                        height=Dimension(**PREVIEW_DIMENSION_DICT),
                    ),
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
            results = self.state["active_collection"].query_records(
                query_str=self.input_str
            )
        except Exception:
            self.results_control.text = ["(invalid query)"]
        else:
            results = sorted(results.keys(), key=results.get, reverse=True)
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
        doc_count_str = ", ".join(
            [f"{row[1]} {row[0].__name__}" for row in _doc_count.values]
        )
        if text is None:
            text = (
                f"{coll.records_db.df.shape[0]} docs in "
                f"{coll.collection_id}: "
                f"{doc_count_str}"
            )
        self.status_bar.text = text

    def update_preview_bar(self, text=None):
        """Update the preview bar text."""
        coll = self.state["active_collection"]
        if text is None:
            text = "preview document"
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
        self.update_results()
        self.update_preview()
        self.update_status_bar()


if __name__ == "__main__":
    """stand-alone window test."""

    coll_ids = Collection.registered_collections()
    collections = [Collection.load(coll) for coll in coll_ids]
    window = SearchView(state={"active_collection": collections[0]})

    @window.kb.add("c-c")
    def _(event):
        event.app.exit()

    with patch_stdout():
        Application(
            layout=window.layout, key_bindings=window.kb, full_screen=True
        ).run()
