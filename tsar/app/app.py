"""
This module contains high level management of:
- views (interactive bits)
- view_models (business logic for views)
- collections (underlying data interface object)
"""
from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from tsar.lib.collection import Collection
from tsar.app.search_window import SearchView, SearchViewModel
from tsar.app.collections_window import CollectionsView
from prompt_toolkit.widgets import HorizontalLine
from prompt_toolkit.layout.containers import HSplit, Window

# create global and page keybindings
from prompt_toolkit.key_binding import KeyBindings, ConditionalKeyBindings, merge_key_bindings


class Screen(object):
    """Class that defines a view (layout, keybindings) and view_model (logic) for a specific screen."""
    pass


class App(object):
    """Contains MVVM style prompt-toolkit views, view models, and keybindings."""

    def __init__(self, collection):

        self.screens = []

        self.kb_global = self.register_global_keybindings()

        self.search_view_model = SearchViewModel(collection)
        self.search_view = SearchView(self.search_view_model)

        self.collections_view_model = None #SearchViewModel(Collection)
        self.collections_view = CollectionsView(self.collections_view_model)

        self.layout = self.search_view.layout
        # self.layout = self.collections_view.layout
        self.kb = self.search_view.kb

        self.application = Application(
            layout=self.layout,
            key_bindings=self.kb_global,
            full_screen=True
        )

    def register_global_keybindings(self):
        """Register global (app-wide) key bindings."""
        kb = KeyBindings()

        @kb.add("q")
        def close_app(event):
            """ctrl+c to quit application. """
            event.app.exit()

        @kb.add("t")
        def next_screen(event):
            """display next screen."""
            self.layout.container.children = self.collections_view.layout.container.children
            self.key_bindings = self.collections_view.kb
        return kb

    def add_screen(self, screen_view, screen_view_model, screen_kb):
        """add screen to list of screens."""


    def run(self):
        self.application.run()



if __name__ == "__main__":

    collection = Collection("wiki")

    app = App(collection)
    app.run()
