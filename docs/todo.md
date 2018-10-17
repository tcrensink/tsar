# V2: to do for refactored/rewritten version
X install elasticsearch
- learn a bit of elasticsearch
- write an abc searcher class skeleton
- figure out how to integrate elastic search and searcher class
- create an environment.yaml, requirements.txt(?), setup.py to generate an environment and start running



# V1
Notes from the first version of TSAR

# Priority stack:
- debug/profile laggy UI
- make a gif for each operation
- bug prevents adding new database (with zero) records
- installation:
    - add .yml/setup.sh for req. install and adding to path
    - consider PyInstaller(?) to make executables for macos, linux, windows.
    - verify install process on other machines
    - consider docker
- clean up code
- add documentation

# Bugs:
- improve scrolling smoothness/selection while holding up/down keys
- Search status bar is not updated after a new record is added
- scrolling goes offscreen with many records
- unable to view long records in DISPLAY mode
- datetime crashes when searched
- search by tags?
- different behavior when Updating a new record, depending on last field

# Functionality/UI:
- improve keys combinations/meta keys for adding/editing records
- fix tab spacing in Edit widgets
- copy selected field to clipboard from DISPLAY (ctrl+c)
- improve messaging on keypresses actions
- clickable links to documents (softlink?) or href for urls

# Features to add:
- sort results (date, alphabetic, top hit)
- add help/shortcut keys/syntax examples page
- major feature: point to folder and index records as files
- design/implement related record browsing
- design/implement quick append feature
- design/implement meta data recording for each record: 
    - view history, edit history, search queries, records accessed on same query (build relational network)
- set default database
- auto-recommend tags (jedi?)
- syntax coloring (jedi?)
- string matching highlighting
- save/access search history with ctrl+left/right
- export records to SQL, pandas, mongo?

# Refactor:
- performance: run in background; call to foreground when calling `tsar`
- implement (extensible) state_machine and observer design patterns for all GUI elements
