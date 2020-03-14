(currently pre-release)

# What is TSAR?
TSAR is a frictionless terminal interface for accessing your custom document collections.  With introspection tools (search as you type, browse) and curation/learning tools (annotation, spaced repetition), your document collections become an extension of your mind.

# Features
**Access**: search and browse documents with filtering, fuzzy search, wildcards, and more:
<img align="center" src="./resources/search2.gif" width=90%>

**Workflow Integration**: TSAR makes a distinction between *documents* (your files) and *records* (document text metadata). This means you can use TSARs search/browse/annotation with any kind of document - markdown, web pages, even images - while still using your favorite text editor/web browser to interact with source documents directly:
<img align="center" src="./resources/workflow1.gif" width=90%>

**Flexibility**: Create multiple *collections* of documents, each with custom search fields, syntax highighting, and preview behavior.  Customize TSAR default behavior, including  default browser, text editor and key bindings.

**Extensibility**: The real power of TSAR lies in *Record Types*.  Use the included library of functions to define how TSAR handles your documents, or write your own.

**Terminal Interface**: TSAR provides a terminal-based interface for ultimate efficiency.  It leverages the powerful prompt-toolkit library with features like auto-suggestion, autocompletion, and syntax highlighting to integrate directly into your workflow.

**Learning tools (coming soon):** The goal of TSAR is larger than just a low-friction data interface; TSAR aims to help you *think with* and *learn from* your data.  Students, researchers, and knowledge-workers will benefit from features like ultra-accessible "capture", and spaced-repetition review.

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
