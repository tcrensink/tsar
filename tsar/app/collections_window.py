#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from __future__ import unicode_literals
from prompt_toolkit.application import Application
# from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_next,
    focus_previous,
)
from prompt_toolkit.layout import HSplit, Layout
# from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea, HorizontalLine
from tsar.lib.collection import Collection
import logging


def button_handler_factory(view_model, collection_name):
    """create callables to bind to each button that updates the active_collection."""
    def handler():
        view_model.update_selected_collection(collection_name)
        logging.info(f"collection set to: {view_model.collection.name}")
    return handler


class CollectionsViewModel(object):
    """Business logic for collections view"""
    def __init__(self, collection):

        self.collection = collection
        self.collection_names = tuple(collection.db_meta.index)

    def update_selected_collection(self, collection_name):
        """sets the active collection and returns it"""
        collection = Collection(collection_name=collection_name)
        self.collection = collection
        return collection


class CollectionsView(object):
    """Bind input, visual elements to search_view_model logic. """

    def __init__(self, collections_view_model):

        self.view_model = collections_view_model
        collection_names = collections_view_model.collection_names

        # create buttons, bind function that returns their name when clicked.
        buttons = []
        for coll_name in collection_names:

            handler = button_handler_factory(self.view_model, coll_name)
            button = Button(f"{coll_name}", handler=handler)
            buttons.append(button)
            if coll_name == self.view_model.collection.name:
                focused_element = button

        root_container = Box(
            HSplit(
                [
                    Label(text='Collections:'),
                    Box(
                        body=HSplit(
                            buttons,
                            padding=1
                        ),
                        padding=2,
                        style='class:left-pane'
                    ),
                ]
            ),
        )

        self.layout = Layout(
            container=root_container,
            focused_element=focused_element
        )

        # Key bindings.
        self.kb = KeyBindings()
        self.kb.add('down')(focus_next)
        self.kb.add('up')(focus_previous)

    def refresh_view(self, collection):
        self.view_model.collection = collection




if __name__ == "__main__":
    """stand-alone version of the collections window for debugging."""

    collection = Collection("wiki")
    view_model = CollectionsViewModel(collection)
    view = CollectionsView(view_model)

    @view.kb.add("c-c")
    def _(event):
        event.app.exit()

    application = Application(
        layout=view.layout,
        key_bindings=view.kb,
        full_screen=True
    )
    application.run()
