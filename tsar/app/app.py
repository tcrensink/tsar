"""
This module contains high level management of:
- views (interactive bits)
- view_models (business logic for views)
- collections (underlying data interface object)
"""
from prompt_toolkit.application import Application
from tsar.lib.collection import Collection
from tsar.lib.search import Server, Client
from tsar.app.search_window import SearchView, SearchViewModel
from tsar.app.collections_window import CollectionsView, CollectionsViewModel
from prompt_toolkit.key_binding import (
    KeyBindings,
    merge_key_bindings
)
from tsar.config import GLOBAL_KB, DEFAULT_COLLECTION, DEFAULT_SCREEN
from tsar import LOG_PATH
import logging


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
    """Contains MVVM style views, view models, and keybindings."""

    def __init__(
        self,
        initial_collection_name=DEFAULT_COLLECTION,
        initial_screen_name=DEFAULT_SCREEN
    ):

        Server().start()
        # empty prompt_toolkit application

        # mutable/updatable object references across app.
        self.shared_state = {
            "active_collection": Collection(initial_collection_name),
            "active_screen": None,
            "prev_screen": None,
            "global_kb": self._return_global_keybindings(),
            "application": Application(full_screen=True),
        }
        # screens in app
        self.screens = {}
        self.screens["search"] = Screen(
            shared_state=self.shared_state,
            ViewModel=SearchViewModel,
            View=SearchView
        )
        self.screens["collections"] = Screen(
            shared_state=self.shared_state,
            ViewModel=CollectionsViewModel,
            View=CollectionsView
        )
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
        return kb_global

    def update_state(self, screen_key):
        """Update shared_state when screen is changed."""
        if self.shared_state["active_screen"] == self.screens[screen_key]:
            return
        self.shared_state["prev_screen"] = self.shared_state["active_screen"]
        self.shared_state["active_screen"] = self.screens[screen_key]
        self.shared_state["application"].layout = self.shared_state["active_screen"].layout
        self.shared_state["application"].key_bindings = merge_key_bindings(
            [
                self.shared_state["active_screen"].key_bindings,
                self.shared_state["global_kb"]
            ]
        )
        self.shared_state["active_screen"].refresh_view()

    def run(self):
        self.shared_state["application"].run()



if __name__ == "__main__":

    """Instantiate views, view_models, app; run the app."""
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
    logging.getLogger('parso.python.diff').disabled = True
    app = App()
    app.run()
