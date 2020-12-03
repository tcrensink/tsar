#!/usr/bin/env python
"""
This module contains high level management of the terminal interface:
- Screen: contains view and view_model for a single window (e.g. search)
- App: manages active view, app state, keybindings, and event loop
"""
import logging
import threading
from tsar.doctypes.doctype import update_dict
from tsar.app.search_view import SearchView
from tsar.app.collections_view import CollectionsView
from tsar.lib.collection import Collection, Register
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application import Application
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.app.rest import FLASK_KWARGS, return_flask_app

RUN_MAIN_APP = True

INITIAL_VIEW = "search"


def return_global_keybindings(app):
    """Register key bindings (global, screen specific)."""
    kb_global = KeyBindings()

    @kb_global.add("c-c")
    def close_app(event):
        event.app.exit()

    @kb_global.add("c-a")
    def collection_view(event):
        app.update_active_view(view=app.state["views"]["collections"])

    @kb_global.add("c-s")
    def search_view(event):
        app.update_active_view(view=app.state["views"]["search"])

    return kb_global


class App(object):
    """Main tsar app."""

    def __init__(self):

        collections = {
            coll_id: Collection.load(coll_id)
            for coll_id in Collection.registered_collections()
        }
        self.global_kb = return_global_keybindings(self)

        # global state dict that objects (e.g. screens) register themselves to and can access.
        self.state = {
            "app": Application(full_screen=True),
            "collections": collections,
            "active_collection": collections[list(collections.keys())[0]],
            "views": {},
        }

        # add screens; self.state must exist before adding but all objects share state ref.
        self.state["views"]["search"] = SearchView(state=self.state)
        self.state["views"]["collections"] = CollectionsView(state=self.state)

        self.state["active_view"] = self.state["views"]["search"]
        self.state["app"].layout = self.state["active_view"].layout
        self.state["app"].key_bindings = merge_key_bindings(
            [self.global_kb, self.state["active_view"].kb]
        )

    def update_active_view(self, view):
        self.state["app"].layout = view.layout
        self.state["active_view"] = view
        self.state["app"].key_bindings = merge_key_bindings([self.global_kb, view.kb])
        view.reset_view()

    def run(self):
        """Start Prompt-toolkit event loop."""
        with patch_stdout():
            self.state["app"].run()


if __name__ == "__main__":
    """Instantiate views, view_models, app; run the app."""

    tsar_app = App()

    # start flask CLI server in a thread
    # flask_app = return_flask_app(tsar_app)

    # log = logging.getLogger("werkzeug")
    # log.disabled = True
    # threading.Thread(target=flask_app.run, kwargs=FLASK_KWARGS).start()

    # start main app; set to false to debug CLI server.
    if RUN_MAIN_APP:
        tsar_app.run()
