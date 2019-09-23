# V2: start with very fast, lightweight experiments on UI, UX

# working, bug-free
    - tsar init: recreate metadata based on content_folder files
    - tsar query: search current records
    - tsar add: copy file(s) from elsewhere into content_folder, add associated metadata
    - tsar edit: edit existing file or create new
    - tsar inspect: create temporary db, index for exploring folder contents

# on `tsar inspect test_content`
    X update query after each keystroke
    X select result with up/down (maintain cursor in query)
    X display preview of selected result
    - open record on selection
    X add records summary info at bottom of screen
        X number of records

# improve usability
    - daemonize/reduce startup time
    - update records only if hash differs
    - caching(?)

# next: test it out, get feedback
    - what works well?
    - what is biggest pain point?
    - how would you re-imagine what it offers?
    - thoughts:
        - improve performance
        - provide search metadata:
            - how many records?
            - keywords, ranked by popularity
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
    - feedback thoughts
        - its slow


(Glorious future/notes)

# interface
examples that may be useful, from python-prompt-toolkit/examples/full-screen/:
- results scrolling: ./simple-demos/cursorcolumn-cursorline.py
- in-page search: pager.py
- change focus: focus.py


# prompt-toolkit integration
**presently aborted** Resume the following if a python-prompt-toolkit front end is of interest.
The example files up through 04_autocomplete_link_to_doc.py should work out of the box, or nearly so.

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

X (draft) TUI (use prompt toolkit!)
    X create a layout with a search bar, results widgets
    X get focus working properly:
        X typing modifies query
        X up/down selects results

X fix prompt-toolkit dependency issue
    X standard version needed for ipython, modified for tsar
    X create forked version in `~`/git/forks
    X recursively rename all references to `prompt_toolkit_dev`
    X conda develop <project name!!> -n tsar
    X verify imports work

X move monkey patched example code to forked repo
    X ElasticSearch completer
    X fix references to prompt_toolkit_dev

- (draft) define I/O for selection
    X populate preview of document for query results
    X creat "live" search/return results when updated string
    - simplify: instead of buffer, use a prompt


    - perform (any) pre-defined function when selecting a completion.  See:
        X create a test_function that writes to file (so as not to conflict with buffer etc)
        - what function is called when completion is *selected*?
            - buffer.apply_completion (doesn't seem to be... and is only connected to mouse completion)
            -
        - buffer.

        - in buffer class, see:
               `def insert_text(self, data: str, overwrite: bool = False,
                        move_cursor: bool = True, fire_event: bool = True) -> None:
            """
            Insert characters at cursor position.
            :param fire_event: Fire `on_text_insert` event. This is mainly used to
                trigger autocompletion while typing.
            """`
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

