
[![tcrensink](https://circleci.com/gh/tcrensink/tsar.svg?style=shield)](https://app.circleci.com/pipelines/github/tcrensink/tsar/)

(beta version coming soon)

# What is TSAR?
The [*memex*](https://en.wikipedia.org/wiki/Memex) is a hypothetical device "in which individuals would compress and store all of their [information]... so that it may be consulted with exceeding speed and flexibility".  Stated differently: a program that makes digital information *so available* that it integrates as a seamless extension of your mind.

TSAR is a terminal-based utility with that vision in mind.  Use it to manage a personal knowledge base (PKB) or notes, as a study aid, or to manage academic papers.  Unlike a note-taking app, TSAR adds a layer of services onto your existing documents rather than managing content directly.

# Features
TSAR includes features that mirror cognitive tasks such as (content) retrieval, association, search/discovery, and review.  Some key features include:
- incremental search: per-keystroke results via the lucene query syntax (elasticsearch)
- link-awareness: linked documents can be parsed/indexed and generate search hits
- document association: browse documents by similarity
- content curation: separate collections with custom folder watch and automatic indexing

# Usage
- Add documents (.md, .txt, arxiv urls) to a collection via the terminal client.  TSAR generates metadata from your docs, leaving source data unmodified.
- Attach to the TSAR terminal interface via the command `tsar`; search, browse, preview, documents in a collection.
- Detach from TSAR via `ctrl-c`. It runs in the background and will resume right where you left off next time.

# Extensibility
Want to include a new kind of document?  Define a new *documents type* (in python) to customize parsing, linking, and search indexing behavior.  TSAR was designed with extensibility in mind.

# Installation and quickstart
1. install [Docker](https://www.docker.com/get-started) desktop on your system
2. clone this repository: `git clone https://github.com/tcrensink/tsar.git`
3. run installation script `python install.py` and follow instructions
4. type `tsar` into a terminal window; it may take a few seconds the first time but is fast to connect, disconnect
5. tsar's query window should appear for the `help_docs` collection; type `*` to see all documents; press return to open one.

# Related
Several existing tools have similar aim or helped inspire TSAR.  Some of these include:

- Emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
