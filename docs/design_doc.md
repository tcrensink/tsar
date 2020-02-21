This document describes the TSAR data model and implementation specifics.

# CORE DEFINITIONS
**doc**: source document, generally of any type that will be abstracted as records in tsar.
**record**: a dict represented by {record_id: {record_def_values}} (not implemented as a class), a row in a tsardb.
**record_def**: defines schema, parser, index mapping and everything else to fully specify doc->record
**TsarDB**: class that contains records of type record_def for a given collection.
**Collection**: main interface class; includes tsar_db and tsar_search attributes associated with a specific collection, and implements all methods that are accessed by the app.
**TsarSearch**: class that handles search index associated with a collection
**App**: UI that handles user input and display.  Still need to define UI flow between modalities.


# DESCRIPTION
(raw) source docs are transformed via a RecordDef(ABC) class into records.  RecordDef defines all behavior for how the source doc is converted to a record, including a parser and index mapping for the search engine.  A Collection is a group of records of the same RecordDef that may be searched/browsed together; multiple collections are ok, and different collections may have the same type.  The Collection class contains all high-level methods and serves as an interface to the App class.  A collection object includes TsarDB and TsarSearch objects as attributes.  The App defines the UI flow/behavior and is not yet determined; it should include the interaction modalities noted in description.md.  Optimally, TSAR runs in the background and is instantly conjured in any terminal window.


# SIMPLIFYING ASSUMPTIONS TO START
- Collections have a fixed schema, search mapping.  use case-switch as needed to parse different files to standard record format.
- use screen to "instantly conjure"; integrate with terminal command if possible.
- ignore multiple collections for now.  You still have `tsar inspect`
- create concrete record_defs before making ABC to get started
- focus on capture, search, review first.  browse, summarize can come later with minimal change to UI.


# USER INTERFACE
- what is user workflow?
    terminal commands:
        - `tsar`: [default action: capture]
        - `tsar capture`: opens capture buffer
        - `tsar query`: opens search/browse interface
        - `tsar inspect <entry_point> <record_def>`: open query interface for docs at entry_point
    in-tsar navigation:
        - capture <-> query (shortcuts)
        - (from query):
            - select record to view, edit
        - (from capture):
            - cmd + n -> new document
            - selected text -> new document


# QUESTIONS, OPEN AND ANSWERED
- Q: how to handle app-state difficuties found in tsar 1.0?
- Q: How to keep Collection organized?  E.g.: I want to add lasso regularization info somewhere - a new doc or is there an existing one that makes sense?
    A: Suggest related docs for adding (SO style for questions)
- Q: Can a collection include different record_defs, or record_defs with different schemas?
    A: No, not now (do not implement this, it will blow up).
- Q: Are source docs copied or linked?
    A: For now, create a "full text" attribute in the tsar_db, a copy of each source doc in the record.
- Q: how to summarize a collection for understanding it as a whole?
- Q: what is the tradeoff of explicit specification vs model inference (e.g., should you prompt the user for keywords or generate them automatically from a new doc?)
    A: As a guiding principle, minimize friction.  Auto generate keywords unless the user overrides (this is advanced feature though).


# EXAMPLE API USAGE
```python
"""
EXAMPLE 1: create new collection, add records:
"""
# defines parser, indexing map, etc; does not uniquely specify the collection:
record_def = WikiRecord()

# create globally unique collection (name), with associated record_def, db, and index:
COLLECTION_NAME = "wiki"
tsar_db = TsarDB(name=COLLECTION_NAME, record_def=record_def)
search_index = SearchIndex(name=COLLECTION_NAME, record_def=record_def)

# Collection aggregates all objects useful for a collection:
collection = Collection(
    name=COLLECTION_NAME,
    record_def=record_def,
    tsar_db=tsar_db,
    search_index=search_index
)

# `add`, `remove` make needed calls to record_def, tsar_db, and search_index objects bound in __init__:
for fp in file_path:
    collection.add(fp)
collection.remove("some_record_id")

"""
EXAMPLE 2: Open existing collection, search/browse records
"""
# load collection with static method (just pickle for now)
collection = Collection.load("wiki_collection.pkl")
results = collection.query("some query string")
related_results = collection.browse(some_record_id)

"""
EXAMPLE 3: how does flow control work with tsar?  How is this mirrored in the code?  TBD.
"""
```

# API SKETCH
Here is a sketch of

```python
# global_config.py
VIEW_PROGRAMS = {
    ".txt": "/path/to/subl",
    ".md": "/path/to/md_viewer_prog",
}
EDIT_PROGRAMS = {
    ".txt": "/path/to/subl",
    ".md": "/path/to/subl",
}

KEYBOARD_SHORTCUTS = {
    "add_new": "ctrl+a",
    "open_in_tsar": "enter",
    "open_out_of_tsar": "shift+enter"
}

# collections.py: dict of collection names and associated paths(?)
_BASE_SCHEMA = {
    "record_id": "str",
    "file_type": "str",
}

class RecordDef(ABC):
    """A "config" class that defines all behavior of a record/collection, notably the record schema.

    ABC implementation not known yet, so pseudo-code below taken with grain of salt:
    """
    self.name
    self.record_schema = # dict
    self.base_schema = BASE_SCHEMA
    self.index_mapping = # https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
    self.browse_config = # ??
    def parser(self, doc):
        """Parse doc to output record (dict) that fulfills record_schema."""

    def base_parser(self, doc):
        """parse default fields required by tsar, such as unique id and filetype (for open/edit prog)"""

    def _validate_parser(self, parse_func, **kwargs):
        """verify parser generates record according to schema"""

    def _validate_search_mapping(self):
        """verify search mapping inputs match schema fields, etc."""


# wiki_record_def.py: instantiation of RecordDef. Use parser_lib.py functions.
class WikiRecord(RecordDef):
    pass

# parser_lib.py: parsing functions to compose dict returned by RecordDef.parser.  Something like:
def read_text_file(filename, base_schema_key1, base_schema_key2):
    # (code to read text and generate base_schema
    # return (text_str, base_schema_key1: base_schema_val1, base_schema_key2: base_schema_val2)

def parse_text(text_str, base_schema_key3, text_col, keyword_col):
    # (code to gen parsed_text)
    # return {text_col: parsed_text, keyword_col: {keywords}, base_schema_key3: }

def read_arxiv(url):
    # (code)...

class TsarDB(object):
    """create tsar_db object associated with collection and associated methods/attributes"""
    def __init__(self, RecordDef, collection_name=None):
        self.collection_name = collection_name
        self.record_def = record_def
        self.df = #(return df from collection if it exists, otherwise empty df)
    def add_record(self, doc):
        pass
    def del_record(self, record):
        pass
    def update_record(self, record):
        pass
    def return_record(self, record_id):
        pass
    @staticmethod
    def load(db_path):
        pass

class TsarSearch(object):
    """Class wraps elasticsearch client and handles search index related manipulations."""
    def __init__(self, RecordDef, collection_name=None):
        self.collection_name = collection_name
    def index_record(self, record):
        """Index provided record; err if schema is not correct."""
        pass
    def del_record(self, record):
        """remove record from index"""
        pass
    def reindex(self, records):


class Collection(object):
    """Main interface class for source docs and app.  This should be only object called to perform high level tasks such as add_record(doc), remove_record, query_records (these call methods in attribute objects).
    """
    def __init__(self, name, record_def, tsar_db, tsar_search)
        pass
    def new_record(self):
        pass
    def add_record(self, doc):
        pass
    def del_record(self, record):
        pass
    def reindex_records(self):
        pass
    def reindex_records(self):
        pass
    def query(self, query_str):
        pass
    def browse(self, record):
        pass
    def return_collection_metadata(self):
        pass


class App(object):
    """The API that handles user input, display.  This is beta; define UI flow first."""
    def __init__(self, tsar_db):
        pass
    def capture(self):
        """opens live content buffer for adding isht"""
        pass
    def search_screen(self):
        pass
    def browse_screen(self):
        pass
    def inspect(self, record_type, path):
        pass
```

