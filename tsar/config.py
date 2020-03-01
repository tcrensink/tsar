"""TSAR config file."""

EDITOR = '/usr/local/bin/subl'
# TSAR_FOLDER = '/Users/trensink/Dropbox/shared_wiki'

ELASTICSEARCH_PORT = 9200

# global keybindings
GLOBAL_KB = {
    "exit": "c-c",
    "search_screen": ("s-right"),
    "collections_screen": ("s-left"),
    "open_document": "enter",
}

# color styles for results list
SEARCH_RECORD_COLORS = {
    'selected': 'bg:#944288',
    'unselected': 'default'
}

DEFAULT_COLLECTION = "wiki"
DEFAULT_SCREEN = "search"
