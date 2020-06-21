"""
A simple example of a few buttons and click handlers.
"""
from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_next,
    focus_previous,
)
from prompt_toolkit.layout import HSplit, Layout
from prompt_toolkit.widgets import Box, Button, Label
from tsar.lib.collection import Collection
from tsar.config import DEFAULT_COLLECTION
from prompt_toolkit.key_binding import merge_key_bindings


class CollectionsViewModel(object):
    """Business logic for collections view"""

    def __init__(self, shared_state):

        self.shared_state = shared_state
        self.collection_names = tuple(shared_state["active_collection"].db_meta.index)


class CollectionsView(object):
    """Bind input, visual elements to search_view_model logic. """

    def __init__(self, collections_view_model):

        self.view_model = collections_view_model
        self.shared_state = self.view_model.shared_state
        collection_names = self.view_model.collection_names

        # create buttons, bind function that returns their name when clicked.
        buttons = []
        for coll_name in collection_names:
            handler = self._button_handler_factory(coll_name)
            button = Button(f"{coll_name}", handler=handler)
            buttons.append(button)
            if coll_name == self.shared_state["active_collection"].name:
                focused_element = button

        root_container = Box(
            HSplit(
                [
                    Label(text="Collections:"),
                    Box(
                        body=HSplit(buttons, padding=1),
                        padding=2,
                        style="class:left-pane",
                    ),
                ]
            ),
        )

        self.layout = Layout(container=root_container, focused_element=focused_element)

        # Key bindings.
        self.kb = KeyBindings()
        self.kb.add("down")(focus_next)
        self.kb.add("up")(focus_previous)

    def _button_handler_factory(self, collection_name):
        """Create handlers to bind to each button when pressed."""

        def handler():
            self.shared_state["active_collection"] = Collection(collection_name)
            # if "collections" is first screen, there will be no prev_screen
            if self.shared_state["prev_screen"] is None:
                self.shared_state["prev_screen"] = self.shared_state["active_screen"]
            self.shared_state["active_screen"] = self.shared_state["prev_screen"]
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

        return handler

    def refresh_view(self):
        pass


if __name__ == "__main__":
    """stand-alone version of the collections window for debugging."""

    shared_state = {
        "active_collection": Collection(DEFAULT_COLLECTION),
        "active_screen": None,
        "application": Application(),
    }
    view_model = CollectionsViewModel(shared_state)
    view = CollectionsView(view_model)

    @view.kb.add("c-q")
    def _(event):
        event.app.exit()

    application = Application(
        layout=view.layout, key_bindings=view.kb, full_screen=True
    )
    application.run()
