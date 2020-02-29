This document describes the TSAR data model and implementation specifics.

# CORE DEFINITIONS
**document**: source document, generally of any type that can be abstracted as records in tsar.
**record**: a dict represented by {record_id: {record_def_values}} (not implemented as a class), a row in a tsardb.
**RecordDef**: defines schema, parser, index mapping and everything else to ingest a source document
**search.Server, search.Client**: classes to interact w/elasticsearch indexes associated with collections
**Data**: database that contains records of type RecordDef for a given collection.
**Collection**: Main interface class between underlying record management and app class.  Each *collection* instance is associated with a RecordDef, database, search index, etc.  Collection class has Data, Client, RecordDef attributes, and presents high-level methods for operations such as: query_records, add_document, open_document, remove_record, browse_records, etc.  Also includes collection-level methods, such as tf-idf keyword generation, browser network generation, etc.
**App**: defines interaction between collections and UI.
**AppWrapper**: handles input, control flow, and screen integration

# BACKEND DESIGN
(raw) source docs are transformed via a RecordDef(ABC) class into records.  RecordDef defines all behavior for how the source doc is converted to a record, including a parser and index mapping for the search engine.  A Collection is a group of records of fixed RecordDef that may be searched/browsed/accessed together; multiple collections are possible, different collections may use the same RecordDef.  The App class makes calls to a Collection instance that implements all record management.  Collection is generally the only class that the App should communicate to.

# FRONTEND DESIGN
Ideally, all stateful data (active_collection, active_record, etc., current_collections) is managed at the app level, alongside a collection of Screens which display it.  This model is complicated when screens can modify app-level data. The following guidelines are used to keep things coherent:
- keep all app-wide data as attributes, as much as possible
- App-level data that is modified via a screen (e.g. active_collection selection) is done via @property
- Currently, `App.update_app()` updates the active screen attributes (colletion) and app attributes (layout, keybindings).  The screen may not be fully reinitialized however; if this is insufficient, then it may be sensible to implement a method `state.refresh_data(self.active_collection, ...)` for all screens.
- Screen is effectively operating as an ABC, and should be converted to one (or otherwise enforce methods)
- The organization of View, ViewModel and collection is working ok, but up for reconsideration.


# UI DESCRIPTION
Optimally, TSAR runs in the background, instantly conjured by a terminal command in any terminal window.  The provisory interface is as follows (see description.md modalities for more thoughts):
**Terminal Commands**
- `tsar` (opens tsar with default action)
- `tsar note` (opens capture interface)
- `tsar query <collection (optional)>`
- `tsar <collection> add <record_id>`: add doc/record_id from which the document can be parsed.
- `tsar inspect <entry_point> <record_def>`: open query interface for docs at entry_point

**Windows**
- Capture: auto-saved buffer.  Selected text converted to doc with kbd shortcut (when applicable).
- Search: live search bar, selectable matched records list, doc preview window.  Select a record to open.
- Browse: combine with query?  Unclear what this would look like in a terminal interface
- Collection Select: choose active collection from dropdown menu.
- Help: show description, keyboard shortcuts

**In-App Keybindings:**
- show keybindings
- add doc (active collection)
- new doc (? if defined in the RecordDef; e.g. opens text document at path)
- rm record (leaves doc alone)


# SIMPLIFYING ASSUMPTIONS TO START
- Collections have a fixed schema, search mapping.  Multiple doc types can be handled in `gen_record` but must output to the same record, mapping schema.
- use screen for fast access for now, or integrate this feature some later time
- ignore App simultaneous handling of multiple collections for now
- create at least three concrete RecordDefs before deciding ABC implementation
- focus on capture, search, review first.  browse, summarize can come later with minimal change to UI.


# QUESTIONS, ANSWERED
- Q: How to keep Collection organized?  E.g.: I want to add lasso regularization info somewhere - a new doc or is there an existing one that makes sense?
    A: Suggest related docs for adding (SO style for questions)
- Q: Can a collection include different record_defs, or record_defs with different schemas?
    A: No; do not implement this.  You can make a union schema, add defaults/null values if you wish to include parsing for multiple file types.
- Q: Are source docs copied or linked?
    A: For now, whatever is easiest.  Management strategy may depend on document types (save a webpage?).
- Q: what is the tradeoff of explicit specification vs model inference (e.g., should you prompt the user for keywords or generate them automatically from a new doc?)
    A: As a guiding principle: minimize friction.  Auto generate keywords unless the user overrides (this is advanced feature though).


# QUESTIONS, OPEN
- Q: how to handle app-state difficuties found in tsar 1.0?
- Q: how to summarize a collection for understanding it as a whole?
- Q: how will you implement browse?  What is the UI?  Will there be a GUI?  Are links user generated or automated?  How will they be updated?:
    - networkX
    - graphdb
    - keywords: semantic inferencing, foward-chaining
    - discussion on knowledge representation: http://graphdb.ontotext.com/documentation/free/introduction-to-semantic-web.html#introduction-to-semantic-web-reasoning-strategies
