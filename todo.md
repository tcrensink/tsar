# WORK COMPLETED LOG
- v1.2 is working, with some bugs.  Try tsar {query, add, init, edit, inspect(!)}
    - inspect a bit buggy
- clarified tsar purpose, functionality, and design in description.md
- clarified api in design_doc.md
- clarified "daemon" operation.  Major findings:
    - `service` package, communicates with background process may be useful (see examples/)
    - http client/server technically works, but client startup is too slow (see examples/)
    - tty, VT100 like client/server model for terminal processes; very difficult to reroute tty
    - for now, dedicated screen instance seems best :/

# TO DO
- RecordDef instance (don't write ABC)
    - class
    - parse_lib

- SearchClient
- TsarDB (as needed)
- Collection (facade for RecordDef, SearchClient, TsarDB)
    - high level functions surfaced to app, e.g. open_record()

- App (prototype)
    - structure
    - capture interface
    - connect query, capture with keystroke (make fast)
    - inspect interface

- (debug, productionize)
    - installation
    - add tests(?)
    - docstrings
    - clear repo history, recreate new
    - make public?
    - add example vids
...
- RecordDef: arxiv
- Prototype browse function
- Prototype review function

