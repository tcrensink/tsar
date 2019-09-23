"""Query/search app interface

- SearchInterface(object):
    - connects tsar_app (including df, tsar_search (elasticsearch) with prompt_toolkit app defined here
    - attributes include query, results, preview layout objects
    - handles index logic for selected results from list
    - includes callback for updating results based on query
- run(tsar_app):
    - defines prompt_toolkit layout, runs prompt_toolkit app
"""

from __future__ import unicode_literals
# import os
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.widgets import HorizontalLine
from functools import partial
from prompt_toolkit.formatted_text import FormattedText
STYLE = {
    'selected': 'bg:#944288',
    'unselected': 'default'
}


class SearchInterface(object):
    """Interface that handles search_page display logic from tsar_app records

    - prompt-toolkit query, results, preview, status elements as attributes
    - generates results from search_page query string
    - formats results for display
    - handles index of selected result
    - generates preview of selected record

    """

    def __init__(self, tsar_app, style=STYLE, index=-1):

        self.tsar_app = tsar_app
        self.query_buffer = Buffer(name='query_buffer', multiline=False)
        # callback function that links query to results:
        self.query_buffer.on_text_changed += self.update_results
        self.results_textcontrol = FormattedTextControl('(no results)')
        self.preview_textcontrol = FormattedTextControl('(no result selected)')
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
            preview_str = self.tsar_app.tsar_db.df.loc[self.results[self.index]]['content']
        self.preview_textcontrol.text = preview_str

    def _update_selected_result(self, old_index, new_index):
        """update formatted results style based on index change.

        old or new index may be -1 or no longer exist
        """
        try:
            self.formatted_results[old_index] = (
                self.style['unselected'],
                self.formatted_results[old_index][1]
            )
        except IndexError:
            pass
        try:
            self.formatted_results[new_index] = (
                self.style['selected'],
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
            formatted_results = [(self.style['unselected'], res)
                                 for res in results_list]
        else:
            formatted_results = []
        return formatted_results

    def update_results(self, passthrough='dummy_arg'):
        """call back function updates results when query text changes
        - signature required to be callable from prompt_toolkit callback

        - set results based on query
        - set formatted results (default formatting)
        - update index to 0 (-1 if no results)
            - updates selected record
            - updates preview of selected record
        - update status bar
        """
        self.results = self.tsar_app.tsar_search.query_records(
            self.query_str,
            self.tsar_app.tsar_db.df
        )
        self.formatted_results = self._apply_default_format(self.results)
        self.results_textcontrol.text = self.formatted_results
        self.index = 0
        self.status_textcontrol.text = '{} of {} records'.format(
            len(self.results),
            self.tsar_app.tsar_db.df.shape[0]
        )


def run(tsar_app):
    """start the interactive search page.query

    LAYOUT: define buffers, assign query -> results callback
    """
    search_interface = SearchInterface(tsar_app)

    query_window = Window(
        BufferControl(
            search_interface.query_buffer
        ),
        height=1,
    )

    result_window = Window(
        search_interface.results_textcontrol,
        # FormattedTextControl(record_selector.results),
        height=12
    )
    preview_window = Window(
        search_interface.preview_textcontrol,
        height=22
    )
    status_window = Window(
        search_interface.status_textcontrol,
        height=1,
        style='reverse'
    )

    line = HorizontalLine()

    # GENERATE LAYOUT
    layout = Layout(
        HSplit([
            Window(
                FormattedTextControl('query:'),
                height=1,
                style='reverse'
            ),
            query_window,
            line,
            result_window,
            line,
            preview_window,
            status_window
        ])
    )

    # KEYBINDINGS
    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        " Control-c to quit application. "
        event.app.exit()

    # select result:
    @kb.add('up')
    @kb.add('down')
    def _(event):
        """change selection based on key presses
        - update selected result (formatted_results.index)
        - update preview
        """
        key = event.key_sequence[0].key
        if key == 'up':
            search_interface.index -= 1
        if key == 'down':
            search_interface.index += 1

    # APPLICATION
    application = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True
    )

    application.run()
