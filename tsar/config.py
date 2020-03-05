"""TSAR config file."""

EDITOR = "/usr/local/bin/subl"

BROWSER = "Safari"
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
    'selected': 'bg:#144288',
    'unselected': 'default'
}

DEFAULT_COLLECTION = "lit"
DEFAULT_SCREEN = "search"

