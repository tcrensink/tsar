
[![tcrensink](https://circleci.com/gh/tcrensink/tsar.svg?style=shield)](https://app.circleci.com/pipelines/github/tcrensink/tsar/)

(deprecated)

# What is TSAR?
Imagine a program that makes your personal digital information *so available* that it becomes a seamless extension of your thought. This was imagined as early as [*memex*](https://en.wikipedia.org/wiki/Memex), a hypothetical device "in which individuals would compress and store all of their [information]... [to be] consulted with exceeding speed and flexibility".

TSAR is a tool designed to facilitate digitally-integrated thinking similar to that of *memex*. It is a terminal app to  access, introspect, curate, and review your digital documents *as efficiently as possible*. Use it to manage a personal knowledge base (PKB), as a study aid for your notes, or help navigate complex project information. Unlike a note-taking app, TSAR provides services for your existing documents rather than managing content directly.

# Features
TSAR includes features that mirror cognitive tasks such as retrieval, association, search/discovery, and review.  Features include:
- incremental search: per-keystroke results with elasticsearch
- linking: browse linked documents (e.g. a markdown wiki) or index linked docs for search relevance (e.g. arxiv link)
- content association: efficiently find associated material that is not explicitly linked
- custom content curation: manage separate collections, each with custom sources (e.g. folders), document types, and indexing
- document type agnostic: a flexible framework allows plain text, markdown, pdf, arxiv papers, etc. to seamlessly interoperate

# Installation and quickstart
1. install [Docker](https://www.docker.com/get-started) desktop on your system
2. clone this repository: `git clone https://github.com/tcrensink/tsar.git`
3. run installation script `python install.py` and follow instructions
4. type `tsar` in a bash shell to launch the interface

# Extensibility
Want to modify how documents are parsed or parse a new kind of document altogether?  The document type engine was designed to be extended with just a bit of python.

# Related
Several tools helped inspire TSAR or have related functionality.  A (very incomplete) list includes:

- Emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
