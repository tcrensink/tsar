"""
module for search screen.

query string search syntax:
https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax
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

class SearchViewModel(object):
    """View model/business logic for search window.

    - prompt-toolkit query, results, preview, status elements as attributes
    - generates results from search_page query string
    - formats results for display
    - handles index of selected result
    - generates preview of selected record
    """

    def __init__(self, shared_state, style=SEARCH_RECORD_COLORS):

        self.shared_state = shared_state
        self.RecordDef = self.shared_state["active_collection"].RecordDef
        self.query_buffer = Buffer(name="query_buffer", multiline=False)
        # callback function that links query to results:
        self.query_buffer.on_text_changed += self.update_results
        self.results_textcontrol = FormattedTextControl("(no results)")
        self.preview_header = BufferControl(
            focusable=False,
        )
        self.preview_header.buffer.text = "RECORD PREVIEW"

        self.preview_textcontrol = BufferControl(
            focusable=False,
            input_processors=[TabsProcessor(tabstop=4, char1=' ', char2=' ')],
            lexer=PygmentsLexer(self.RecordDef.preview_lexer)
        )
        self.preview_textcontrol.lexer.style = self.RecordDef.preview_style
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
        """update preview content based on index
        """
        if self.index == -1:
            preview_str = "(no result selected)"
        else:
            record = self.shared_state["active_collection"].df.loc[self.results[self.index]]

            id_str = f"RECORD_ID:\t\t{record['record_id']}\n"
            _kw_str = ', '.join(sorted(record['keywords']))
            kw_str = f"KEYWORDS:\t\t{_kw_str}\n"
            date = datetime.fromtimestamp(record["utc_last_access"])
            _date_str = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
            access_date_str = f"LAST ACCESS:\t{_date_str}\n"
            summary_str = f"\n{record['record_summary']}"
            preview_str = id_str + kw_str + access_date_str + summary_str

        self.preview_textcontrol.buffer.text = preview_str

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
            # results_list = [f"{res}\n" for res in results_list]
            result_names = self.shared_state['active_collection']\
                .df.loc[results_list].record_name
            results_list = [f"{res}\n" for res in result_names]
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
        try:
            results = self.shared_state["active_collection"]\
                .query_records(self.query_str)
            self.results = sorted(results, key=itemgetter(1), reverse=True)
        except Exception:
            self.results = {}
            self.status_textcontrol.text = "(invalid query)"
        else:
            self.formatted_results = self._apply_default_format(self.results)
            self.results_textcontrol.text = self.formatted_results
            self.index = 0
            self.status_textcontrol.text = (
                f"showing {len(self.results)} of "
                f"{self.shared_state['active_collection'].df.shape[0]} records.    "
                f"(ref: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax)"
            )

    def open_selected(self):
        """open selected record
        """
        if len(self.results) > 0:
            record_id = self.results[self.index]
        else:
            pass
        self.shared_state["active_collection"]\
            .open_document(record_id=record_id)
        self._update_preview_content()


class SearchView(object):
    """Bind input, visual elements to search_view_model logic. """

    def __init__(self, search_view_model):

        self.view_model = search_view_model
        self.shared_state = self.view_model.shared_state

        # layout components:
        self.query_header = Window(
            FormattedTextControl(query_title_bar_text(self.shared_state)),
            height=1,
            style="reverse"
        )

        self.query_window = Window(
            BufferControl(
                self.view_model.query_buffer,
            ),
            height=1,
        )
        results_window = Window(
            self.view_model.results_textcontrol,
            height=13
        )

        preview_header = Window(
            self.view_model.preview_header,
            height=1,
            style="reverse"
        )

        preview_window = Window(
            self.view_model.preview_textcontrol,
            height=22,
            wrap_lines=True
        )
        status_window = Window(
            self.view_model.status_textcontrol,
            height=1,
            style="reverse"
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
                    status_window
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
            """open selected record"""
            try:
                self.view_model.open_selected()
            except Exception:
                self.view_model.status_textcontrol.text = "(no doc selected)"

    def refresh_view(self):
        """Code when screen is changed."""
        # self.view_model.query_str = ""
        self.query_header.content.text =\
            query_title_bar_text(self.shared_state)
        self.view_model.update_results()
        self.layout.focus(self.query_window)


def query_title_bar_text(shared_state):
    """return text for title bar, updated when screen changes."""
    # cols = shared_state["active_collection"].df.columns
    client = shared_state["active_collection"].client
    coll_name = shared_state["active_collection"].name
    mapping = client.return_fields(coll_name)
    map_fields = mapping.keys()

    fields_str = ' | '.join(map_fields)
    str_value = f"QUERY    fields: {fields_str}"
    return str_value


if __name__ == "__main__":
    """stand-alone version of the search window for debugging."""

    shared_state = {
        "active_collection": Collection(DEFAULT_COLLECTION),
        "active_screen": None,
        "application": Application(),
    }

    view_model = SearchViewModel(shared_state)
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
