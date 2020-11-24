
[![tcrensink](https://circleci.com/gh/tcrensink/tsar.svg?style=shield)](https://app.circleci.com/pipelines/github/tcrensink/tsar/)

(beta version for macos coming soon)

# What is TSAR?
TSAR is a tool to seamlessly integrate your thoughts and digital documents.  It brings services like incremental search, linking, document association, and spaced-repetition to your existing documents in a frictionless text-based interface.  Use it to manage notes, a personal knowledge base (PKB), or as a study aid.

# Usage
- Add documents (.md, .txt, arxiv urls) to a collection via the terminal client.  TSAR generates metadata from your docs, leaving source data unmodified.
- Attach to the TSAR terminal interface via the command `tsar`; search, browse, preview, your documents with unmatched efficiency.
- Detach from TSAR via `ctrl-c`. It runs in the background and will resume right where you left off next time.

# Features
- **Incremental search**: via lucene query syntax, powered by elasticsearch
- **Linking**: Automatically detect and index linked content (hyperlink, citations, etc.)
- **Flexibility**: supports multiple document collections, custom keybindings, folder watch, and more
- **Extensibility**: customize how documents are parsed, link syntax, and more.  TSAR was designed with extensibility in mind.

# Installation and quickstart
1. install [Docker](https://www.docker.com/get-started) desktop on your system
2. clone this repository: `git clone https://github.com/tcrensink/tsar.git`
3. run installation script `python install.py` and follow instructions
4. type `tsar` into a terminal window; it may take a few seconds the first time but is fast to connect, disconnect
5. tsar's query window should appear for the `help_docs` collection; type `*` to see all documents; press return to open one.

# Related
There are several productivity tools with similar goals.  Here are some:

- Emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [nvALT](https://nvultra.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
