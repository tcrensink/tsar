
[![tcrensink](https://circleci.com/gh/tcrensink/tsar.svg?style=shield)](https://app.circleci.com/pipelines/github/tcrensink/tsar/)

(under construction)

# What is TSAR?
Imagine a program that makes digital information *so available* that it becomes a seamless extension of your thought.  This was imagined as early as [*memex*](https://en.wikipedia.org/wiki/Memex), a hypothetical device "in which individuals would compress and store all of their [information]... and consulted with exceeding speed and flexibility".  Modern search engines partially fulfill this vision with unprecedented information retrieval, but aren't tailored to the information *you* care about, and aren't designed to curate, remember, or learn new information.

TSAR is terminal-based utility with the vision of "digitally-integrated thinking" in mind.  More plainly, it is a collection of services to help you curate, manage, introspect, and learn from digital documents *as efficiently as possible*. Use it to manage a personal knowledge base (PKB), as a study aid for your notes, or help organize academic papers.  Unlike a note-taking app, TSAR adds a layer of services onto your existing documents rather than managing content directly.

# Features
TSAR includes features that mirror cognitive tasks such as (content) retrieval, association, search/discovery, and review.  Some key features include:
- incremental search: per-keystroke results via the lucene query syntax (elasticsearch)
- link-awareness: linked documents can be parsed/indexed and generate search hits
- document association: browse documents by similarity
- custom content curation: manage separate collections, each with custom sources (e.g. folders), document types, and indexing
- document-type agnostic framework: search, association, and linking behavior can be specified and interoperate on a per-document-type basis

# Installation and quickstart
1. install [Docker](https://www.docker.com/get-started) desktop on your system
2. clone this repository: `git clone https://github.com/tcrensink/tsar.git`
3. run installation script `python install.py` and follow instructions
4. type `tsar` into a terminal window; it may take a few seconds the first time but remains running in the background
5. tsar's query window should appear for the `help_docs` collection; type `*` to see all documents; press return to open one.

# Extensibility
Want to include a new kind of document?  Define a new *documents type* (in python) to customize parsing, linking, and search indexing behavior.  TSAR was designed with extensibility in mind.

# Related
Several existing tools have similar aim or helped inspire TSAR.  Some of these include:

- Emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
