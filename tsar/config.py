"""TSAR config file."""

# SYSTEM INTEGRATION
EDITOR = "/usr/local/bin/subl"
BROWSER = "Safari"
ELASTICSEARCH_PORT = 9200

# TSAR CONTENT DEFAULTS
DEFAULT_COLLECTION = "arxiv"
DEFAULT_SCREEN = "search"

# GLOBAL KEY BINDINGS
GLOBAL_KB = {
    "exit": "c-c",
    "search_screen": ("c-right"),
    "collections_screen": ("c-left"),
    "open_document": "enter",
}

# STYLING
SEARCH_RECORD_COLORS = {
    'selected': 'bg:#144288',
    'unselected': 'default'
}

