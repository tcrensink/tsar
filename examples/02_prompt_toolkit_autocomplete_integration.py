"""
Integrate with prompt toolkit.  Specifically:
- accept query string
- (live) display results in float (middle of page)
- focus moves to selectable results

notes on completion objects:

Completer: ABC Meta class for defining Completer classes, e.g. standard behavior for word/sql completion
ElasticSearchCompleter(Completer): class definition that performs query on string to popuate results
CompleteEvent: event that triggers autocompletion
Completion: how/what is completed (e.g., what string is inserted at what point in the document)
"""
from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
# from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    HSplit,
    Window,
)
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
# from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea

from typing import Callable, Dict, Iterable, List, Optional, Pattern, Union
from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document
from tsar.lib import search


class ElasticSearchCompleter(Completer):
    """
    "Autocomplete" elasticsearch results based on query string.
    :param query_string: query string
    :param meta_dict: Optional dict mapping words to their meta-text. (This
        should map strings to strings or formatted text.)
    :param pattern: Optional regex. When given, use this regex
        pattern instead of default one.
    """
    def __init__(self,
                 query_string: Union[List[str], Callable[[], List[str]]],
                 query_transform,
                 meta_dict: Optional[Dict[str, str]] = None,
                 pattern: Optional[Pattern[str]] = None,
                 ) -> None:

        self.query_transform = query_transform
        self.query_string = query_string
        self.meta_dict = meta_dict or {}
        self.pattern = pattern

    def get_completions(self, document: Document, complete_event: CompleteEvent) -> Iterable[Completion]:

        query_string = document.text_before_cursor
        results = self.query_transform(query_str=query_string)

        for result in results:
            display_meta = self.meta_dict.get(result, '')
            yield Completion(result, -len(query_string), display_meta='(meta) ' + result)
            # yield Completion(result, -len(query_string), display_meta=display_meta)


es = search.es_client()
def result_preview(query_str, es=es, n_char=100):
    results_dict = es.search(q=query_str)
    df = search.results_to_df(results_dict)
    if df.empty:
        previews = []
    else:
        previews = df.source_body.str[0:n_char] + '...'
    return previews


def main():

    query_completer = ElasticSearchCompleter(query_string='', query_transform=result_preview)

    kb = KeyBindings()

    @kb.add('q')
    @kb.add('c-c')
    def _(event):
        " Quit application. "
        event.app.exit()

    buff = Buffer(completer=query_completer, complete_while_typing=True)
    body = FloatContainer(
        content=HSplit(
            [
                Window(FormattedTextControl('Enter search query (e.g. `*`); results below:'), height=1, style='reverse'),
                Window(BufferControl(buffer=buff)),
                Window(FormattedTextControl("(q to quit)"), height=2, style='default'),
            ]
        ),
        floats=[
            Float(
                left=1,
                xcursor=False,
                ycursor=False,
                content=CompletionsMenu(
                    scroll_offset=1
                )
            )
        ]
    )

    application = Application(
        layout=Layout(body),
        key_bindings=kb,
        full_screen=True)

    application.run()


if __name__ == '__main__':
    main()
