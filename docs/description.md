# WHY TSAR?
You want faster access and deeper understanding of large volumes of human-interpretable records.  Whether data you create (PKR, personal journal, code repo) or a semi-structured document collections of docs (Arxiv, github, etc.), you want better search, faster recall, and improved browsing of some corpus; TSAR provides a frictionless interface and a suite of learning tools to augment your ability to interact with such data.

# INTERACTION MODALITIES
- capture: "digital paper", thought formulation; frictionless current.md from which docs can seamlessly be generated
- search: interactive, with filters and keywords; used for rapid discovery or "fuzzy" lookup
- browse: surface "adjacent" documents;
- inspect: browse documents _not_ in a collection.  Option to add to a collection?  E.g., look at Arxiv, save .pdf locally if you're interested.
- summarize: provide landscape at *collection* level
- review: spaced repetition, reminders, etc.; push data from docs to your brain
- reflection^\*: guided interaction/"conversation" mode used to revisit ideas, reflect on docs, etc.  Concept incomplete.


# USE CASES/EXAMPLES
- **PKR**: You want to fast access to the catelog of knowledge you have acquired over the years.  TSAR provides search and browse functionality to compile your own wiki and blazing fast interface to search it.
- **Study Aid**: From class notes to interview prep questions, use TSAR learning tools to internalize the records.  Add to them or edit them just as easily.
- **Data Discovery**: use an exiting template or write your own record definition to parse a collection of documents and interact with using the TSAR interface.  For example, a Arxiv parser lets you live-search recent publications, browse, or take notes.
- **Data comprehension**: auto-generated browsing and collection summarization help make sense of large corpuses of unexplored records.  Whether document review for law, perusing papers on Arxiv or job listings on linkedIn, TSAR can help make sense of the records landscape.


# ADDITIONAL FEATURES
- semantic thought modalities: capture, search, browse, review
- extensible; define custom parsers to search any kind of record, provided it can be converted to a text-based record.  Interact with source docs using your editor of choice
- performant: runs in the background and is always ready to respond quickly
- terminal-based: closer to terminal-based workstream, lightweight, cross platform, and cross ssh!


# WISHLIST FEATURES
- journaling function(?): template that is filled every day
- search sorting by predefined filters, e.g. add date, edit date, relevance, hits
- syntax coloring in custom preview
- scrolling in search results
- color coding by record: percentage diff, importance, etc.
- "notes" section on records (meta info display for records/docs)
- tool for modifying relational graph?
- clipboard integration
- syntax highlighting


# SERIOUSLY WISHFUL THINKING
- remote access/ssh inspect
- cross platform, synced (linux, mac os, ios)
- really performant/compiled (go? cpp?)
- enterprise ready?
- plug-in ecosystem?
- exposes NLP api\*: (this is not a complete concept yet)
- distributed\*: a team of members can interact with the same collection at the same time
- memory palace\*: visual representation of where each document lives in the collection


# What are similar tools and how is TSAR distinct?
- **org mode**: (unknown)
- **Roam**: (unknown)
- **nvALT**: Tsar is doc-type agnostic, terminal interface (ssh?) and curation tools
- **Google/Chrome bookmarks**: Tsar can be used locally, with curation tools for your collections
- **Simple Note/Notes (mac)/...**: (unknown)
- **confluence/wiki.js**: Tsar has (faster) terminal access, is doc-type extensible, adds curation tools.

- vs local files + grep: a "poor man's" TSAR.  TSAR should simply be more usable and have additional features.
- vs Evernote: TSAR is extensible, terminal based, and faster(?)
- emacs org-mode: TSAR is editor independent, with greater focus on data curation and introspection than task management.
