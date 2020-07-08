#!/usr/bin/env python
"""
This module contains high level management of the terminal interface:
- Screen: contains view and view_model for a single window (e.g. search)
- App: manages active view, app state, keybindings, and event loop
"""
from tsar import CAPTURE_DOC_PATH
from tsar.lib.collection import Collection
from tsar.app.search_window import SearchView, SearchViewModel
from tsar.app.collections_window import CollectionsView, CollectionsViewModel
from tsar.app.query_source_window import QuerySourceView, QuerySourceViewModel
from tsar.config import GLOBAL_KB, DEFAULT_COLLECTION, DEFAULT_SCREEN, EDITOR
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application import Application
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.lib.record_defs.parse_lib import open_textfile
from tsar.lib.record_defs.wiki_record import WikiRecord


class Screen(object):
    """Define object necessary to determine app state and change view.

    This should be an ABC, defining template for future screens.
    """

    def __init__(self, shared_state, ViewModel, View):
        self.shared_state = shared_state
        self.view_model = ViewModel(shared_state)
        self.view = View(self.view_model)
        self.key_bindings = self.view.kb
        self.layout = self.view.layout
        self.refresh_view = self.view.refresh_view


class App(object):
    """Contains MVVM style views, view models, and keybindings.

    Organization:
    - shared_state includes the prompt_toolkit application and state values shared globally in App
    - shared_state includes values that may be modified by a Screen for example
    - self.screens contains Screen objects, e.g. search_screen or collections_screen.  These contain layouts
    - app.layout is dynamically bound to Screen layouts in app.update_state().  Screens have their own global logic which is also called.
    - calls to app.update_state are defined (and triggered) via app._return_global_keybindings()
    """

    def __init__(
        self,
        initial_collection_name=DEFAULT_COLLECTION,
        initial_screen_name=DEFAULT_SCREEN,
    ):
        if "default_collection" not in Collection.db_meta().index:
            Collection.new(collection_name="default_collection", RecordDef=WikiRecord)

        # mutable/updatable object references across app.
        self.shared_state = {
            "Collection": Collection,
            "active_collection": Collection(initial_collection_name),
            "active_screen": None,
            "prev_screen": None,
            "global_kb": self._return_global_keybindings(),
            "application": Application(full_screen=True),
        }

        # app screens
        self.screens = {
            "collections": Screen(
                shared_state=self.shared_state,
                ViewModel=CollectionsViewModel,
                View=CollectionsView,
            ),
            "search": Screen(
                shared_state=self.shared_state,
                ViewModel=SearchViewModel,
                View=SearchView,
            ),
            "source_query": Screen(
                shared_state=self.shared_state,
                ViewModel=QuerySourceViewModel,
                View=QuerySourceView,
            ),
        }
        self.update_state(initial_screen_name)
        self.shared_state["active_screen"] = self.screens[initial_screen_name]

    def _return_global_keybindings(self):
        """Register key bindings (global, screen specific)."""
        kb_global = KeyBindings()

        @kb_global.add(GLOBAL_KB["exit"])
        def close_app(event):
            event.app.exit()

        @kb_global.add(GLOBAL_KB["search_screen"])
        def search_screen(event):
            self.update_state("search")

        @kb_global.add(GLOBAL_KB["collections_screen"])
        def collections_screen(event):
            self.update_state("collections")

        @kb_global.add(GLOBAL_KB["open_capture_doc"])
        def open_capture(event):
            open_textfile(path=CAPTURE_DOC_PATH, editor=EDITOR)

        @kb_global.add(GLOBAL_KB["source_query"])
        def add_screen(event):
            self.update_state("source_query")

        return kb_global

    def update_state(self, screen_key):
        """Update shared_state when screen is changed."""
        if self.shared_state["active_screen"] == self.screens[screen_key]:
            return

        self.shared_state["prev_screen"] = self.shared_state["active_screen"]
        self.shared_state["active_screen"] = self.screens[screen_key]
        self.shared_state["application"].layout = self.shared_state[
            "active_screen"
        ].layout
        self.shared_state["application"].key_bindings = merge_key_bindings(
            [
                self.shared_state["active_screen"].key_bindings,
                self.shared_state["global_kb"],
            ]
        )
        self.shared_state["active_screen"].refresh_view()

    def run(self):
        """Start Prompt-toolkit event loop."""
        with patch_stdout():
            self.shared_state["application"].run()


if __name__ == "__main__":
    """Instantiate views, view_models, app; run the app."""

    app = App()
    app.run()
