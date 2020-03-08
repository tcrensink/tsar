# What is TSAR?
TSAR is a frictionless terminal interface for interacting with large collections of documents.  Search, browse, and edit your document collections from a single interface.


# Key features
**Discovery**: search and browse documents as you type, using boolean operators, filtering, fuzzy search, wildcards, and regex.  Powered by elasticsearch.

**Workflow**: Unlike many notetaking apps or productivity tools, TSAR makes a distinction between *documents* (source data of interest) and *records* (metadata asscociated with each document).  Doing so allows TSAR to provide a unified interface for introspection that is completely agnostic to the document file type; TSAR lets you use your favorite text editor/web browser to interact with documents.

**Extensibility**: The real power of TSAR lies in the definition of *Record Types*.  Use a library of functions to define how metadata is generated from your source documents, or create your own.

**Flexibility**: Define multiple, semantically different *Collections* that can be explored independently, with distinct search indexing, syntax highighting, etc.

**Learning tools (coming soon):**  The ultimate aim of TSAR is to augment your mastery over the information in curated data sets.  To that end, a host of learning tools, from raw information "capture" methods to spaced-repetition review are included to help ingest information in your corpera.

**Terminal Interface**: TSAR leverages the python prompt-toolkit for a fast and feature-rich text-basd interface ready at the terminal.


# Example use-cases
- **Journal/Personal Knowledge Base**: Catelog and curate knowledge accrued over the years.  Any document is only a few keystrokes away.
- **Information Discovery**: Use TSAR to efficiently introspect external document repositories such as Arxiv or Github.

# Installation
Currently requires installation of Elasticsearch and several python dependencies.  Packaging coming soon.

# Related

TSAR grew out of a desire to create the perfect productivity tool for learning and remembering large volumes of information.  Sources of inspiration and related tools include:

- ["Getting Things Done"](https://gettingthingsdone.com) by David Allen
- emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [nvALT](https://nvultra.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
