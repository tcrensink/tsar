#!/usr/bin/env python
"""
This module contains high level management of the terminal interface:
- Screen: contains view and view_model for a single window (e.g. search)
- App: manages active view, app state, keybindings, and event loop
"""
import logging
import threading
from tsar import CAPTURE_DOC_PATH
from tsar.lib.collection import Collection, Register
from tsar.app.search_window import SearchView, SearchViewModel
from tsar.app.collections_window import CollectionsView, CollectionsViewModel
from tsar.app.query_source_window import QuerySourceView, QuerySourceViewModel
from tsar.config import GLOBAL_KB, DEFAULT_COLLECTION, DEFAULT_SCREEN, OPEN_TEXT_CMD
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application import Application
from prompt_toolkit.patch_stdout import patch_stdout
from tsar.lib.record_defs.parse_lib import open_textfile
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
        app.update_state("search")

    @kb_global.add(GLOBAL_KB["collections_screen"])
    def collections_screen(event):
        app.update_state("collections")

    @kb_global.add(GLOBAL_KB["open_capture_doc"])
    def open_capture(event):
        open_textfile(cmd=OPEN_TEXT_CMD, file_path=CAPTURE_DOC_PATH)

    @kb_global.add(GLOBAL_KB["source_query"])
    def add_screen(event):
        app.update_state("source_query")

    return kb_global


class App(object):
    """Main tsar app."""

    def __init__(self,):

        self.collections = {
            coll_id: Collection.load(coll_id)
            for coll_id in Collection.registered_collections()
        }
        default_coll = list(self.collections.values())[0]

        self.app = Application(full_screen=True)
        self.state = {
            "app": self.app,
            "active_collection": default_coll,
            "active_screen": None,
            "key_bindings": return_global_keybindings(self),
            "collections": {
                coll_id: {"query_str": "*", "selected_doc": None, "results": [],}
                for coll_id in self.collections.keys()
            },
            "screens": {"search_screen": None},
        }

        # ViewScreen1(state=self.state)
        # self.state["app"].layout = ViewScreen1.layout

    def update_window(self, screen_key):
        pass

    # def update_state(self, screen_key):
    #     """Update shared_state when screen is changed."""
    #     if self.shared_state["active_screen"] == self.screens[screen_key]:
    #         return
    #     self.shared_state["prev_screen"] = self.shared_state["active_screen"]
    #     self.shared_state["active_screen"] = self.screens[screen_key]
    #     self.shared_state["application"].layout = self.shared_state[
    #         "active_screen"
    #     ].layout
    #     self.shared_state["application"].key_bindings = merge_key_bindings(
    #         [
    #             self.shared_state["active_screen"].key_bindings,
    #             self.shared_state["global_kb"],
    #         ]
    #     )
    #     self.shared_state["active_screen"].refresh_view()

    def run(self):
        """Start Prompt-toolkit event loop."""
        with patch_stdout():
            self.app.run()


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
