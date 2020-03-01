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

    def __init__(self, collection, ViewModel, View):
        self._collection = collection
        self.view_model = ViewModel(self._collection)
        self.view = View(self.view_model)
        self.key_bindings = self.view.kb
        self.layout = self.view.layout
        self.refresh_view = self.view.refresh_view

    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, collection):
        self._collection = collection
        self.view_model.collection = collection


class App(object):
    """Contains MVVM style views, view models, and keybindings."""

    def __init__(
        self,
        default_collection_name=DEFAULT_COLLECTION,
        default_screen=DEFAULT_SCREEN
    ):

        Server().start()
        # empty application updated in update_screen
        self.application = Application()
        self._active_collection = Collection(default_collection_name)
        self._global_kb = self._return_global_keybindings()
        self.kb = self._global_kb

        # add screens to app:
        self.screens = {}
        self.screens["search"] = Screen(
            collection=self._active_collection,
            ViewModel=SearchViewModel,
            View=SearchView
        )
        self.screens["collections"] = Screen(
            collection=self._active_collection,
            ViewModel=CollectionsViewModel,
            View=CollectionsView
        )
        self.active_screen = None
        self.active_screen = self.update_state(default_screen)

    @property
    def active_collection(self):
        """active collection is always pulled from the collections screen"""
        self._active_collection = self.screens["collections"].view_model.collection
        return self._active_collection

    @active_collection.setter
    def active_collection(self, active_collection):
        self._active_collection = active_collection

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

    def _update_keybindings(self):
        """Merge and return keybindings for global + screen."""
        kb = merge_key_bindings(
            [self._global_kb, self.active_screen.key_bindings]
        )
        return kb

    def update_state(self, screen_key):
        """On keystroke, display new screen with current data."""

        if self.active_screen == self.screens[screen_key]:
            return
        self.active_screen = self.screens[screen_key]
        # self.active_screen.collection = self.active_collection
        self.active_screen.refresh_view(collection=self.active_collection)
        self.application.layout = self.active_screen.layout
        self.application.key_bindings = self._update_keybindings()

    def run(self):
        self.application.run()


if __name__ == "__main__":

    """Instantiate views, view_models, app; run the app."""
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
    logging.getLogger('parso.python.diff').disabled = True
    app = App()
    app.run()
