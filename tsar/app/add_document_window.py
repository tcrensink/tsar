"""Window for adding a document to the current collection."""

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


def dummy(dummy_str):
    import ipdb

    ipdb.set_trace()


class AddDocumentViewModel(object):
    """View model/business logic for add_doc window."""

    def __init__(self, shared_state, style=SEARCH_RECORD_COLORS):

        self.shared_state = shared_state
        self.RecordDef = self.shared_state["active_collection"].RecordDef
        self.input_buffer = Buffer(
            name="input_buffer", multiline=False, accept_handler=self.add_document
        )
        # callback function that links input to results:
        self.input_buffer.on_text_changed += self.update_results
        self.results_textcontrol = FormattedTextControl("(no results)")
        self.preview_header = BufferControl(focusable=False,)
        self.preview_header.buffer.text = "DOCUMENT PREVIEW"

        self.preview_textcontrol = BufferControl(
            focusable=False,
            input_processors=[TabsProcessor(tabstop=4, char1=" ", char2=" ")],
            lexer=PygmentsLexer(self.RecordDef.preview_lexer),
        )
        self.preview_textcontrol.lexer.style = self.RecordDef.preview_style
        self.preview_textcontrol.buffer.text = "(no document selected)"
        self.status_textcontrol = FormattedTextControl()
        self.style = style
        # value -1 indicates no result is currently selected
        self._index = -1
        self.results = []
        # FormattedText results:
        self.formatted_results = self._apply_default_format(self.results)
        self.update_results()

    @property
    def input_text(self):
        return self.input_buffer.text

    @input_text.setter
    def input_text(self, new_input_text):
        """computes results when set
        """
        self.input_buffer.text = new_input_text

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
            preview_str = "(no document selected)"
        else:
            record = self.shared_state["active_collection"].df.loc[
                self.results[self.index]
            ]

            id_str = f"RECORD_ID:\t\t{record['record_id']}\n"
            _kw_str = ", ".join(sorted(record["keywords"]))
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
            # results_list = [f"{res}\n" for res in results_list]
            result_names = (
                self.shared_state["active_collection"].df.loc[results_list].record_name
            )
            results_list = [f"{res}\n" for res in result_names]
            formatted_results = [
                (self.style["unselected"], res) for res in results_list
            ]
        else:
            formatted_results = []
        return formatted_results

    def update_results(self, passthrough="dummy_arg"):
        """call back function updates results when input text changes
        - signature required to be callable from prompt_toolkit callback

        """
        pass
        # try:
        #     record = self.RecordDef.gen_record(self.input_text)
        #     self.preview_textcontrol.buffer.text = "something here"
        # except ValueError:
        #     self.preview_textcontrol.buffer.text = "nothing here"

    def add_document(self, record_id):
        """Add document associated with record_id.

        behavior governed by accept_handler of Buffer:
        https://python-prompt-toolkit.readthedocs.io/en/master/pages/reference.html?highlight=accept_handler#module-prompt_toolkit.buffer

        if bool(return_val) buffer text is erased, otherwise retained.
        """
        try:
            self.shared_state["active_collection"].add_document(record_id=record_id)

            return_val = None
        except Exception:
            pass
            return_val = True
        return return_val


class AddDocumentView(object):
    """Bind input, visual elements to search_view_model logic. """

    def __init__(self, add_document_view_model):

        self.view_model = add_document_view_model
        self.shared_state = self.view_model.shared_state

        # layout components:
        self.window_header = Window(
            FormattedTextControl(title_bar_text(self.shared_state)),
            height=1,
            style="reverse",
        )

        self.query_window = Window(
            BufferControl(self.view_model.input_buffer,), height=1,
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
                    self.window_header,
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
            self.view_model.input_text = ""

    def refresh_view(self):
        """Code when screen is changed."""
        # self.view_model.input_text = ""
        self.window_header.content.text = title_bar_text(self.shared_state)
        self.view_model.update_results()
        self.layout.focus(self.query_window)


def title_bar_text(shared_state):
    """return text for title bar, updated when screen changes."""
    # cols = shared_state["active_collection"].df.columns
    title_str = "Add document to: {}".format(shared_state["active_collection"].name)
    return title_str


if __name__ == "__main__":
    """stand-alone version of the search window for debugging."""

    shared_state = {
        "active_collection": Collection(DEFAULT_COLLECTION),
        "active_screen": None,
        "application": Application(),
    }

    view_model = AddDocumentViewModel(shared_state)
    view = AddDocumentView(view_model)

    @view.kb.add("c-q")
    def _(event):
        event.app.exit()

    application = Application(
        layout=view.layout, key_bindings=view.kb, full_screen=True
    )
    application.run()
