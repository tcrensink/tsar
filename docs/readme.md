(currently pre-release)

# What is TSAR?
TSAR is a frictionless terminal interface for large document collections.  With introspection tools (search, browse), and curation/learning tools (fast "capture" mode, spaced repetition), TSAR lets you access digital documents as an extension of your mind.

# Key features
**Discovery**: search and browse documents as you type, using boolean operators, filtering, fuzzy search, wildcards, and regex.  Powered by elasticsearch.

**Workflow**: TSAR makes a distinction between *documents* (source data of interest) and *records* (TSAR's text representation of each document).  In contrast to many notetaking apps, TSAR lets you search/browse/annotate documents of any file-type with the same TSAR interface and open them with your favorite editor/web browser.

**Extensibility**: The real power of TSAR lies in the definition of *Record Types*.  Use the included library of functions to define how metadata is generated/displayed from your source documents, or write your own.

**Flexibility**: Define multiple, semantically different *Collections* that can be explored independently, with distinct search indexing, syntax highighting, etc.

**Terminal Interface**: TSAR provides a terminal-based interface for ultimate efficiency.  It leverages the powerful prompt-toolkit library with features like auto-suggestion, autocompletion, and syntax highlighting to integrate directly into your workflow.

**Learning tools (coming soon):**  TSAR's ultimate aim is to provide the strongest connection possible between your mind and your managed digital collections.  To that end, a host of curation tools are included to help learn the data, if desired.


# Example use-cases
- **Journal/Personal Knowledge Base**: Catelog and curate knowledge accrued over the years.  Any document is only a few keystrokes away.
- **Information Discovery**: Use TSAR to efficiently introspect external document repositories such as Arxiv or Github.

# Installation
Requires Elasticsearch and several python dependencies; deployment coming soon.

# Related
TSAR grew out of a desire to create the perfect productivity tool for interacting with more data than you can remember easily.  Sources of inspiration and related tools include:

- ["Getting Things Done"](https://gettingthingsdone.com) by David Allen
- Emacs [org mode](https://orgmode.org)
- [Roam](https://roamresearch.com)
- [nvALT](https://nvultra.com)
- [wiki.js](https://wiki.js.org)
- [anki](https://www.google.com/search?client=safari&rls=en&q=anki&ie=UTF-8&oe=UTF-8)
- [Mendeley](https://www.mendeley.com/?interaction_required=true)
- [Arxiv sanity preserver](https://www.google.com/search?client=safari&rls=en&q=arxiv+sanity+preserver&ie=UTF-8&oe=UTF-8)
