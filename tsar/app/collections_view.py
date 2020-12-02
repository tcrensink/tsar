"""Collection summary/selection screen."""
from collections.abc import Sequence
from fuzzywuzzy import fuzz
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


class CollectionsView(object):
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
        self.preview_buffer = BufferControl(input_processors=[TabsProcessor(tabstop=4, char1="", char2="")], focusable=False,)
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

        @self.kb.add("enter")
        def _(event):
            collection = self.state["collections"][self.results_control.selected_result]
            self.state["active_collection"] = collection
            self.reset_view()


    @property
    def input_str(self):
        return self.input_buffer.text

    @input_str.setter
    def input_str(self, text):
        self.input_buffer.text = text

    def update_results(self, unused_arg=""):
        """Update self.results in-place."""

        collections = Collection.registered_collections()
        results = {coll: fuzz.ratio(coll, self.input_str) for coll in collections}
        results = sorted(results.keys(), key=results.get, reverse=True)

        self.results_control.text = results
        self.results_control.index = 0
        self.update_preview()

    def update_header_bar(self, text=None):
        """Update the header text."""
        if text is None:
            text = f"Active collection: {state['active_collection'].collection_id}"
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
                f'"{coll.collection_id}": '
                f"{doc_count_str}"
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
        try:
            coll = self.state["collections"][self.results_control.selected_result]
            preview = coll.preview()
        except KeyError:
            preview = f"(no preview available)"
        self.preview_buffer.buffer.text = preview

    def reset_view(self):
        """Update all values from shared state dict."""
        self.update_header_bar()
        self.update_preview_bar()
        self.update_preview()
        self.update_status_bar()
        self.update_results()


if __name__ == "__main__":
    """stand-alone window test."""

    # coll_ids = Collection.registered_collections()
    collections = {coll_id: Collection.load(coll_id) for coll_id in Collection.registered_collections()}
    state = {
        "app": Application(full_screen=True),
        "collections": collections,
        "active_collection": collections[list(collections.keys())[0]],
    }
    window = CollectionsView(state=state)

    @window.kb.add("c-c")
    def _(event):
        event.app.exit()

    with patch_stdout():
        Application(
            layout=window.layout, key_bindings=window.kb, full_screen=True
        ).run()
