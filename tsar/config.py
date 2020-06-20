"""TSAR config file."""
from tsar import REPO_PATH

# SYSTEM INTEGRATION
EDITOR = "/usr/local/bin/code"
BROWSER = "Safari"
ELASTICSEARCH_PORT = 9200

# TSAR CONTENT DEFAULTS
DEFAULT_COLLECTION = "default_collection"
DEFAULT_SCREEN = "search"

# GLOBAL KEY BINDINGS
GLOBAL_KB = {
    "exit": "c-q",
    "search_screen": ("c-right"),
    "collections_screen": ("c-left"),
    "open_document": "enter",
    "open_capture_doc": ("c-a"),
}

# STYLING
SEARCH_RECORD_COLORS = {"selected": "bg:#144288", "unselected": "default"}
