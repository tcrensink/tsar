# Priority stack:
X add .gif to readme with displayed shortcut keys
- use PyInstaller to make standalone, portable executable.  Test on different builds.
- brief code clean up
- profile performance, prioritize bugs

# Bugs:
- improve scrolling smoothness/selection while holding up/down
- Search status bar is not updated after a new record is added
- scrolling goes offscreen for several records
- unable to view long records in DISPLAY mode
- datetime crashes when searched
- search by tags?
- different behavior when Updating a new record, depending on last field

# Functionality:
- sort results (date, alphabetic, top hit)
- copy selected field to clipboard from DISPLAY (ctrl+c)
- improve messaging on keypresses actions
- restore default query string with ctrl x
- clickable links to documents (softlink?) or href for urls

# Features:
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
