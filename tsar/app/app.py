#!/usr/bin/env python
"""
This module contains high level management of the terminal interface:
- Screen: contains view and view_model for a single window (e.g. search)
- App: manages active view, app state, keybindings, and event loop
"""
import logging
import threading
from tsar.app.window import ViewScreen
from tsar.config import GLOBAL_KB
from tsar.lib.collection import Collection, Register
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application import Application
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.app.rest import FLASK_KWARGS, return_flask_app

RUN_MAIN_APP = True


def return_global_keybindings(app):
    """Register key bindings (global, screen specific)."""
    kb_global = KeyBindings()

    @kb_global.add(GLOBAL_KB["exit"])
    def close_app(event):
        event.app.exit()

    @kb_global.add(GLOBAL_KB["search_screen"])
    def search_screen(event):
        pass

    return kb_global


class App(object):
    """Main tsar app."""

    def __init__(self):

        collections = {
            coll_id: Collection.load(coll_id)
            for coll_id in Collection.registered_collections()
        }
        default_coll = list(collections.values())[0]

        self.global_kb = return_global_keybindings(self)

        # define *data* state: collections, string values, etc
        self.state = {
            "app": Application(full_screen=True),
            "collections": {
                coll_id: {"query_str": "*", "selected_doc": None, "results": [],}
                for coll_id in collections.keys()
            },
            "active_collection": default_coll,
        }

        # update with *view* elements; screens, etc
        screens = {
            "search_screen": ViewScreen(state=self.state)
        }
        self.state.update(
            {
                "screens": screens,
                "active_screen": screens["search_screen"],
            }
        )
        self.state["app"].layout = self.state["active_screen"].layout
        self.state["app"].key_bindings = merge_key_bindings([self.global_kb, self.state["active_screen"].kb])

    def update_window(self, screen_key):
        pass

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
