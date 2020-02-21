# WHY TSAR?
You want faster access and deeper understanding of large volumes of human-interpretable records.  Whether data you create (PKR, personal journal, code repo) or a semi-structured document collections of docs (Arxiv, github, etc.), you want better search, faster recall, and improved browsing of some corpus; TSAR provides a frictionless interface and a suite of learning tools to augment your ability to interact with such data.

# INTERACTION MODALITIES
- capture: "digital paper", thought formulation; frictionless current.md from which docs can seamlessly be generated
- search: interactive, with filters and keywords; used for rapid discovery or "fuzzy" lookup
- browse: surface "adjacent" documents;
- summarize: provide landscape at *collection* level
- review: spaced repetition, reminders, etc.; push data from docs to your brain
- reflection^\*: guided interaction/"conversation" mode used to revisit ideas, reflect on docs, etc.  Concept incomplete.

# USE CASES/EXAMPLES
- **PKR**: You want to fast access to the catelog of knowledge you have acquired over the years.  TSAR provides search and browse functionality to compile your own wiki and blazing fast interface to search it.
- **Study Aid**: From class notes to interview prep questions, use TSAR learning tools to internalize the records.  Add to them or edit them just as easily.
- **Data Discovery**: use an exiting template or write your own record definition to parse a collection of documents and interact with using the TSAR interface.  For example, a Arxiv parser lets you live-search recent publications, browse, or take notes.
- **Data comprehension**: auto-generated browsing and collection summarization help make sense of large corpuses of unexplored records.  Whether document review for law, perusing papers on Arxiv or job listings on linkedIn, TSAR can help make sense of the records landscape.


# OTHER FEATURES
- extensible; define custom parsers to search any kind of record, provided it can be converted to a text-based record.  Interact with source docs using your editor of choice
- performant: runs in the background and is always ready to respond quickly
- terminal-based: closer to terminal-based workstream, lightweight, cross platform, and cross ssh!
- exposes NLP api\*: (this is not a complete concept yet)
- distributed\*: a team of members can interact with the same collection at the same time
- memory palace\*: visual representation of where each document lives in the collection
- supports latex\*
- clipboard integration\*
- syntax highlighting\*

# WISHLIST FEATURES
- journaling function(?): template that is filled every day
- syntax coloring in custom preview
- search sorting by predefined filters, e.g. add date, edit date, relevance, hits
- scrolling in search results
- color coding by record: percentage diff, importance, etc.
- "notes" section on records (meta info display for records/docs)
- tool for modifying relational graph?


# SERIOUSLY WISHFUL THINKING
- cross platform, synced (linux, mac os, ios)
- more performant (go? cpp?)
- enterprise ready?
- plug-in ecosystem?


# What are similar tools and how is TSAR distinct?
- vs Google/bookmarked browser/spotlight: TSAR restricts domain to highly relevant docs (for PKR), has different interface, and additional tooling for data curation.  It is also extensible.
- vs Stack Overflow: TSAR is more general than a snippet manager.  Consider making a stack_overflow `record_type` and pulling from the API...  if so, the command line interface might even be faster than opening the browser.
- vs confluence/wiki: tsar should be 1) faster 2) terminal interface 3) doc type extensible
- vs local files + grep: a "poor man's" TSAR.  TSAR should simply be more usable and have additional features.
- vs Evernote: TSAR is extensible, terminal based, and faster(?)
- emacs org-mode: TSAR is editor independent, with greater focus on data curation and introspection than task management.
- nvALT: similar aim - extreme efficiency!  tsar is more than note-taking: it is doc-type indep., extensible, and can be used as an introspection interface to any collection.