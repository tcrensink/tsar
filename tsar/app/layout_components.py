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
