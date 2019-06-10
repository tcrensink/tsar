# V2: start with very fast, lightweight experiments on UI, UX
# Resume test_script.py
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

X (draft) write repl to query records, sanity check elasticsearch
    X prompt for query
    X result prompt to requery or display contents
    X prompt to remove record
    X display results names (fix hits display)

X (draft) add record in terminal from editor
    X define editor excutable in config file
    X open editor when "+" is pressed
    X on save or close, adds document to index (updates index)

X (draft) sync index to markdown files:
    X .md and index reference; both exist
    X add index id when file is created; store at uuid path
    X update index id when file is edited
    X remove index id when file is removed

- (draft) TUI (use prompt toolkit!)
    X create a layout with a search bar, results widgets
    X get focus working properly:
        X typing modifies query
        X up/down selects results

- (draft) define I/O for selection
    X populate preview of document for query results
    X creat "live" search/return results when updated string
    - perform (any) pre-defined function on selection
    - open document on selection (what key?)

- (draft) integrate prompt-toolkit with REPL:
    - file can be viewed via keystroke (ok to view in any program)
    - file can be edited, updated in index (subl)
    - document can be deleted
    - record can be added (assumptions/simplifications ok)

- refactor
    - move files to reasonable place (uncertain at this point...)
    - remove clutter
    - add docstrings
    - lint

- create v0 app
    - create keybindings as needed
    - make TSAR (bash) executable
    - on startup: check for elasticsearch instance, start one if not running
    - create environment.yaml/setup.py or whatever
    - git tag, packge, distribution ready
    - hone widgets
    - add help page

- test
    - debug
    - make a list of highest priority things to change based on usability

- LATER...
    - look back at use-cases in docs
    - add browsing and memory palace capability?
    - improve search results
    - define file-naming system (dated? UUID?, user submitted title?)
    - add lexer for Lucene query syntax
    - add spaced repetition algo/reminder

