# DONE LOG
- working commands: tsar {init, query, add, edit, inspect}
    - inspect a bit buggy
- clarified objectives, design in description.md
- redefined api in design_doc.md

# TO RESUME
- start implementing new API, referencing design_doc api sketch:
    - write RecordDef(ABC)
    - (re)write TsarDB
    - (re)write TsarSearch
    - write Collection
    - test Collection code; write up as tests(?)
    - define App api, behavior
        - reread description.md and think about UI for modalities
        - define desired UI flow in words, document it
        - sketch App api, CLI commands
        - implement App


- read api_sketch.py (almost finished) in prep for refactor.  RecordType and app are the largest changes
- finish implementing REST API search.py
    X instantiate session
    X delete index
    X create index (from template)
    - \_query index (raw)
    - query_index (return list of \_id of records)
    - index_record
    - index_records
    - configure mapping to make use of Elasticsearch text filters for indexing

- write ABC-based RecordType
- create a wiki collection file including:
    - RecordType subclass
    - base_schema definition
    - schema definition
    - start of parsing library
    - elasticsearch mapping

- create config files (start with python files).  See design_doc.md for thoughts
    - global config:
        - editor
        - document collections
        - default document collection
        - default file extension -> record type map
    - document collection
        - name (defines db, index references)
        - default file extension -> record type map
        - default search behavior (which fields are searched by default?)
    - record type definition
        - db parser
            - transformation function
            - fields, types
        - index mapping (parse of metadata to elasticsearch index)

- daemonize:
    - connect to (existing) process for fast access
    - decouple daemon logic (indexing, etc) from program
    - improve results preview (crop filename, show other metadata)
    - add status bar with keywords
    - daemonize to reduce start up time (always on feeling)
    - keep folder structure for wiki files (avoid name collisions)
    - write code base parser


# LATER: after trial, evaluation
    Do this process:
    1) reread tsar raison d'etre, proposed use-cases.  How does it measure up?  Has this vision changed?
        - what works well?
        - what is biggest pain point?
        - how would you re-imagine what it offers?
        - search record previews
        - interactive search
        - journal function?
        - templates?
        - review scheduler?
        - learn/test search syntax.  by keyword? date?
        - improve parser
            - keyword generation with tf-idf?
        - load time/daemonize
        - doc browse/association?
    3) define a clear vision for the architecture.  It should include the following:
        - what is defined by a template, how extensible is it?
        - is there a single tsar, or several different?  Can one include multiple doc types?
        - do files live in a specific folder, or are they just soft-linked?
        - what is the interface workflow?  Will it remain a series of bash commands, or interactive windows?
            - is browse a separate window from search?
            - can you access multiple functions in one session, or each a separate bash command?


(Glorious future/notes)

# interface
examples that may be useful, from python-prompt-toolkit/examples/full-screen/:
- results scrolling: ./simple-demos/cursorcolumn-cursorline.py
- in-page search: pager.py
- change focus: focus.py


# PREVIOUS
X see aborted previous efforts in git/repos/prompt_toolkit, 04_autocomplete_link_to_doc.py

X install elasticsearch
X write elasticsearch example:
    X generate document (string repr of json)
    X index document
    X search for document
    X retrieve document in full

X write elasticsearch example to query local markdown
    X get all .md files from base folder
    X generate elasticsearch doc for each file
    X add doc to elasticsearch index with using client

X (draft) TUI (use prompt toolkit!)
    X create a layout with a search bar, results widgets
    X get focus working properly:
        X typing modifies query
        X up/down selects results

    - perform (any) pre-defined function when selecting a completion.  See:
        X create a test_function that writes to file (so as not to conflict with buffer etc)
        - what function is called when completion is *selected*?
            - buffer.apply_completion (doesn't seem to be... and is only connected to mouse completion)
            -
        - buffer.
