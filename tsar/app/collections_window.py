"""
module for collections screen.
"""

from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import HorizontalLine
from tsar.config import SEARCH_RECORD_COLORS, DEFAULT_COLLECTION
from tsar.lib.collection import Collection
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.layout.processors import TabsProcessor
from datetime import datetime
from operator import itemgetter


class CollectionsViewModel(object):
    """View model/business logic for collections window (based on SearchViewModel)."""

    def __init__(self, shared_state, style=SEARCH_RECORD_COLORS):

        self.shared_state = shared_state
        self.query_buffer = Buffer(name="query_buffer", multiline=False)
        # callback function that links query to results:
        self.query_buffer.on_text_changed += self.update_results
        self.results_textcontrol = FormattedTextControl("(no results)")
        self.preview_header = BufferControl(focusable=False,)
        self.preview_header.buffer.text = "preview"

        self.preview_textcontrol = BufferControl(
            focusable=False,
            input_processors=[TabsProcessor(tabstop=4, char1=" ", char2=" ")],
        )
        self.preview_textcontrol.buffer.text = "(no result selected)"
        self.status_textcontrol = FormattedTextControl()
        self.style = style
        # value -1 indicates no result is currently selected
        self._index = -1
        self.results = []
        # FormattedText results:
        self.formatted_results = self._apply_default_format(self.results)
        self.update_results()

    @property
    def query_str(self):
        return self.query_buffer.text

    @query_str.setter
    def query_str(self, new_query_str):
        """computes results when set
        """
        self.query_buffer.text = new_query_str

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        """defines the index (int) of the selected result
        if no selected result, index=-1 (keeping type int makes life simpler)
        """
        old_index = self._index

        L = len(self.results)
        if L == 0:
            new_index = -1
        elif new_index < 0:
            new_index = 0
        elif L - 1 < new_index:
            new_index = L - 1

        self._index = new_index
        self._update_preview_content()

        # update results formatting
        self._update_selected_result(old_index, new_index)

    def _update_preview_content(self):
        """Update preview content based on index."""
        if self.index == -1:
            preview_str = "(no result selected)"
        else:
            record = (
                self.shared_state["Collection"].db_meta().loc[self.results[self.index]]
            )
            preview_str = str(record)
        self.preview_textcontrol.buffer.text = preview_str

    def _update_selected_result(self, old_index, new_index):
        """update formatted results style based on index change.

        old or new index may be -1 or no longer exist
        """
        try:
            self.formatted_results[old_index] = (
                self.style["unselected"],
                self.formatted_results[old_index][1],
            )
        except IndexError:
            pass
        try:
            self.formatted_results[new_index] = (
                self.style["selected"],
                self.formatted_results[new_index][1],
            )
        except IndexError:
            pass

    def _apply_default_format(self, results_list):
        """convert a list of result strings to a FormattedText object

        print formatted results using print_formatted_text
        """
        if len(results_list) != 0:
            result_names = results_list
            results_list = [f"{res}\n" for res in result_names]
            formatted_results = [
                (self.style["unselected"], res) for res in results_list
            ]
        else:
            formatted_results = []
        return formatted_results

    def update_results(self, passthrough="dummy_arg"):
        """call back function updates results when query text changes
        - signature required to be callable from prompt_toolkit callback

        - set results based on query
        - set formatted results (default formatting)
        - update index to 0 (-1 if no results)
            - updates selected record
            - updates preview of selected record
        - update status bar
        """
        try:
            results = self.shared_state["Collection"].db_meta().index
            self.results = sorted(results)
        except Exception:
            self.results = {}
            self.status_textcontrol.text = "(invalid query)"
        else:
            self.formatted_results = self._apply_default_format(self.results)
            self.results_textcontrol.text = self.formatted_results
            self.index = 0
            self.status_textcontrol.text = (
                f"showing {len(self.results)} of "
                f"{self.shared_state['Collection'].db_meta().shape[0]} collections"
            )

    def select_collection(self):
        """Set active collection."""
        if len(self.results) > 0:
            collection = self.results[self.index]
        else:
            pass
        self.shared_state["active_collection"] = Collection(collection_name=collection)
        self._update_preview_content()


class CollectionsView(object):
    """Bind input, visual elements to collections_view_model logic. """

    def __init__(self, collections_view_model):

        self.view_model = collections_view_model
        self.shared_state = self.view_model.shared_state

        # layout components:
        self.query_header = Window(
            FormattedTextControl(return_title_bar_text(self.shared_state)),
            height=1,
            style="reverse",
        )

        self.query_window = Window(
            BufferControl(self.view_model.query_buffer,), height=1,
        )
        results_window = Window(self.view_model.results_textcontrol, height=13)

        preview_header = Window(
            self.view_model.preview_header, height=1, style="reverse"
        )

        preview_window = Window(
            self.view_model.preview_textcontrol, height=22, wrap_lines=True
        )
        status_window = Window(
            self.view_model.status_textcontrol, height=1, style="reverse"
        )

        # GENERATE LAYOUT
        self.layout = Layout(
            HSplit(
                [
                    self.query_header,
                    self.query_window,
                    results_window,
                    preview_header,
                    preview_window,
                    status_window,
                ]
            ),
        )

        # SEARCH PAGE KEYBINDINGS
        self.kb = KeyBindings()

        # select result:
        @self.kb.add("up")
        def _(event):
            self.view_model.index -= 1

        @self.kb.add("down")
        def _(event):
            self.view_model.index += 1

        @self.kb.add("escape")
        def _(event):
            self.view_model.query_str = ""

        @self.kb.add("enter")
        def _(event):
            """set active collection"""
            try:
                self.view_model.select_collection()
            except Exception:
                self.view_model.status_textcontrol.text = "(no collection selected)"

    def refresh_view(self):
        """Code when screen is changed."""
        self.query_header.content.text = return_title_bar_text(self.shared_state)
        self.view_model.update_results()
        self.layout.focus(self.query_window)


def return_title_bar_text(shared_state):
    """return text for title bar, updated when screen changes."""
    str_value = f"COLLECTIONS"
    return str_value


if __name__ == "__main__":
    """stand-alone version of the collections window for debugging."""

    shared_state = {
        "Collection": Collection,
        "active_collection": Collection(DEFAULT_COLLECTION),
        "active_screen": None,
        "application": Application(),
    }

    view_model = CollectionsViewModel(shared_state)
    view = CollectionsView(view_model)

    @view.kb.add("c-q")
    def _(event):
        event.app.exit()

    application = Application(
        layout=view.layout, key_bindings=view.kb, full_screen=True
    )
    application.run()
