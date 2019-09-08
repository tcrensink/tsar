"""query interface that executes query callback on keystrokes.


Todo: decouple result selection from result data management

RecordSelector current manages result formatting and the selected result index,
while results_from_query is a standalone function that returns a list of result strings.

Separate the functionality more clearly between result managment and selection managment as follows:

class result_selector: only defines logic of selected result index
    - attr for number of results, current result
    - methods for changing result index

class ResultManager:
    - init:
        - tsar_app (contains all result data from a query)
        - result_selector (manages result selection)
    - attr selected_index: defines current result, with help of result_selector
    - method formatted_results: returns list of FormattedText results
    - method `preview`: generates/returns preview of selected result
"""

from __future__ import unicode_literals

import os
from prompt_toolkit import prompt
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


def return_status_text(num_results, num_records):
    """
    """
    status_str =  "{num_results} of {num_records} |\
    ".format(num_results=3, num_records=3)


class RecordSelector(object):
    """convert list of results to FormattedText list of tuples; index defines selected row.
    """
    def __init__(self, results_list=None, style=STYLE, index=None):

        self.style = style
        if results_list is None:
            results_list = []
        # results must always be modified in-place
        self.results = []
        self.update_results(
            results_list=results_list,
            index=index
        )

    @property
    def result_styles(self):
        _result_styles, _ = zip(*self.results)
        return list(_result_styles)

    @property
    def result_texts(self):
        _, _result_texts = zip(*self.results)
        return list(_result_texts)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        """change the results `style` based active_result_index
        """
        # self._index may not exist:
        try:
            old_index = self._index
        except AttributeError:
            old_index = None

        # correct value bounds:
        try:
            if new_index >= len(self.results):
                new_index = len(self.results) - 1
            elif new_index < 0:
                new_index = 0
        except TypeError:
            pass
        self._index = new_index
        self._update_selected(old_index, new_index)

    def _update_selected(self, old_index, new_index):
        """change the style of previous index to default, new index to selected
        Either old or new index may be None and should be handled separately
        """
        if len(self.results) == 0:
            return
        try:
            _, res = self.results[old_index]
            self.results[old_index] = (self.style["unselected"], res)
        except TypeError:
            pass
        try:
            _, res = self.results[new_index]
            self.results[new_index] = (self.style["selected"], res)
        except TypeError:
            pass

    def _apply_default_format(self, results_list):
        """convert a list of result strings to a FormattedText object

        print formatted results using print_formatted_text
        """
        results_list = ["{}\n".format(res) for res in results_list]
        formatted_results = FormattedText([(self.style['unselected'], res) for res in results_list])
        return formatted_results

    def update_results(self, results_list, index=None):
        """update attributes from new results_list.  It's critical
        that the results object maintains the same id, else they will not be updated.
        """
        self.results.clear()
        self.results.extend(self._apply_default_format(results_list))
        self.index = index


def results_from_query(
    query_buffer,
    tsar_app,
    record_selector,
):
    """get results from query, update formatted_results object
    """
    result_record_ids = tsar_app.tsar_search.query_records(
        query_buffer.text,
        tsar_app.tsar_db.df
    )
    results_list = []
    rec_str = "{n} {name}, {summary}"
    for j, record_id in enumerate(result_record_ids):
        record = tsar_app.tsar_db.df.loc[record_id]
        name = os.path.split(record.name)[1]
        summary = record.file_path
        results_list.append(rec_str.format(n=j, name=name, summary=summary))

    record_selector.update_results(results_list)

def return_preview(
    record_id,
    tsar_db,
):
    """return a preview based on the current result index
    """
    preview = tsar_db.df.loc[record_id].content
    return preview



def run(tsar_app):
    """LAYOUT: define buffers, assign query -> results callback"""

    query_window = Window(
        BufferControl(
            Buffer(
                name='query_buffer',
                multiline=False
            )
        ),
        height=1,
    )

    record_selector = RecordSelector()
    result_window = Window(
        FormattedTextControl(record_selector.results),
        height=12
    )

    preview_window = Window(
        FormattedTextControl('(no record preview yet)'),
        height=22
    )

    status_window = Window(
        FormattedTextControl('{} of {} records'.format(1, tsar_app.tsar_db.df.shape[0])),
        height=1,
        style='reverse'
    )

    line = HorizontalLine()


    """ DEFINE CALLBACKS
    - update results from query
    - update status bar from query
    """
    query_window.content.buffer.on_text_changed += partial(
        results_from_query,
        tsar_app=tsar_app,
        record_selector=record_selector,
    )


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

    ### KEYBINDINGS
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
        import pdb; pdb.set_trace()
        key = event.key_sequence[0].key
        try:
            if key == 'up':
                record_selector.index -= 1
            if key == 'down':
                record_selector.index += 1
        except TypeError:
            record_selector.index = 0
        preview_window.content = return_preview(
            record_id=tsar_app.tsar_db.df.iloc[record_selector.index],
            tsar_db=tsar_app.tsar_db,
        )


    ### APPLICATION
    application = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=True)

    application.run()

