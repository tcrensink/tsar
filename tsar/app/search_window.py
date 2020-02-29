"""Query/search app interface.

SearchInterface: defines behavior and coupling of search page and tsar_app
run: runs/starts the search_page application
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
from tsar.config import SEARCH_RECORD_COLORS
from tsar.lib.collection import Collection


class SearchViewModel(object):
    """View model/business logic for search window.

    - prompt-toolkit query, results, preview, status elements as attributes
    - generates results from search_page query string
    - formats results for display
    - handles index of selected result
    - generates preview of selected record
    """
    def __init__(self, collection, style=SEARCH_RECORD_COLORS):

        self.collection = collection
        self.query_buffer = Buffer(name="query_buffer", multiline=False)
        # callback function that links query to results:
        self.query_buffer.on_text_changed += self.update_results
        self.results_textcontrol = FormattedTextControl("(no results)")
        self.preview_textcontrol = FormattedTextControl("(no result selected)")
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
        """update preview content based on index
        """
        if self.index == -1:
            preview_str = "(no result selected)"
        else:
            preview_str = self.collection.df.loc[self.results[self.index]]["record_summary"]
        self.preview_textcontrol.text = preview_str

    def _update_selected_result(self, old_index, new_index):
        """update formatted results style based on index change.

        old or new index may be -1 or no longer exist
        """
        try:
            self.formatted_results[old_index] = (
                self.style["unselected"],
                self.formatted_results[old_index][1]
            )
        except IndexError:
            pass
        try:
            self.formatted_results[new_index] = (
                self.style["selected"],
                self.formatted_results[new_index][1]
            )
        except IndexError:
            pass

    def _apply_default_format(self, results_list):
        """convert a list of result strings to a FormattedText object

        print formatted results using print_formatted_text
        """
        if len(results_list) != 0:
            results_list = ["{}\n".format(res) for res in results_list]
            formatted_results = [(self.style["unselected"], res)
                                 for res in results_list]
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
        results = self.collection.query_records(self.query_str)
        self.results = list(results.keys())

        self.formatted_results = self._apply_default_format(self.results)
        self.results_textcontrol.text = self.formatted_results
        self.index = 0
        self.status_textcontrol.text = f"{len(self.results)} of {self.collection.df.shape[0]} records"

    def open_selected(self):
        """open selected record
        """
        if len(self.results) > 0:
            record_id = self.results[self.index]
        else:
            pass
        # io.open_record(record_id=record_id)


class SearchView(object):
    """Bind input, visual elements to search_view_model logic. """

    def __init__(self, search_view_model):

        query_window = Window(
            BufferControl(
                search_view_model.query_buffer
            ),
            height=1,
        )
        result_window = Window(
            search_view_model.results_textcontrol,
            height=12
        )
        preview_window = Window(
            search_view_model.preview_textcontrol,
            height=22
        )
        status_window = Window(
            search_view_model.status_textcontrol,
            height=1,
            style="reverse"
        )

        # GENERATE LAYOUT
        self.layout = Layout(
            HSplit(
                [
                    Window(
                        FormattedTextControl("query:"),
                        height=1,
                        style="reverse"
                    ),
                    query_window,
                    HorizontalLine(),
                    result_window,
                    HorizontalLine(),
                    preview_window,
                    status_window
                ]
            )
        )

        # SEARCH PAGE KEYBINDINGS
        self.kb = KeyBindings()

        # select result:
        @self.kb.add("up")
        def _(event):
            search_view_model.index -= 1

        @self.kb.add("down")
        def _(event):
            search_view_model.index += 1

        @self.kb.add("enter")
        def _(event):
            """open selected record"""
            search_view_model.open_selected()


if __name__ == "__main__":
    """stand-alone version of the search window for debugging."""

    collection = Collection("wiki")
    view_model = SearchViewModel(collection)
    view = SearchView(view_model)

    @view.kb.add("c-c")
    def _(event):
        event.app.exit()

    application = Application(
        layout=view.layout,
        key_bindings=view.kb,
        full_screen=True
    )
    application.run()