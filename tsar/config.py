"""TSAR config file."""
from tsar import REPO_PATH

# SYSTEM INTEGRATION
EDITOR = "/usr/local/bin/code"
BROWSER = "Safari"
ELASTICSEARCH_PORT = 9200

# TSAR CONTENT DEFAULTS
DEFAULT_COLLECTION = "help_docs"
DEFAULT_SCREEN = "search"

# GLOBAL KEY BINDINGS
GLOBAL_KB = {
    "exit": "c-c",
    "collections_screen": ("c-a"),
    "source_query": ("c-d"),
    "search_screen": ("c-s"),
    "open_capture_doc": ("c-z"),
    "open_document": "enter",
}

# STYLING
SEARCH_RECORD_COLORS = {"selected": "bg:#144288", "unselected": "default"}
