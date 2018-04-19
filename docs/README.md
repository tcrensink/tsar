<!-- # Screen shots/ Demo -->

# Introducing TSAR: the Textual Storage And Retrieval utility
Tsar is a terminal based snippet manager with features and an interface to help you store and retrieve information *as quickly as possible*.  Tsar currently uses search-as-you-type query, but has plans for sorting, filtering, and associated record browsing.  Some suggested use cases:
- a searchable, general purpose snippet database for fast recall at the command line
- a repository of short code snippets or oft-used bash commands that are hard to remember
- a searchable daily journal/diary
- ...anything else where fast storage/retrieval of information from terminal is a priority.

# Compatibility and Support
Tsar is currently in early beta, running on python 3.x for MacOS.  Support for Linux and backward compatibility for python 2.x is planned for future releases.

# Getting Started
- Installation: download the tsar repository to your computer and run `installation.sh`.
- from a terminal application, call `tsar` with no arguments to open the default database (currently a tutorial db, but customizable).
- Create a new database by copying `./config_files/default_config.py` to `./config_files/my_database_config.py`; call `tsar my_database` from terminal to use it.  The config file will generate an indexed database at `./index_files/my_database` on the first use.

# Q: How does TSAR compare with similar snippet managers?  Why bother with another?
Tsar aims to provide *the fastest* storage and retrieval of information sippets from a terminal workflow, acting as a digital extension of your memory when trying to recall information.  This is achieved via design choices (minimal, keyboard friendly interface) and powerful retrieval aids (the advanced Whoosh search engine, tagging, browsing, etc.).  There are a number of related productivity features intended for future releases.

# Similar projects and inspiration
If you like tsar, you may also be interested in similar workflow productivity tools:
- [bro pages](http://bropages.org): the concise, crowd-sourced, example-based alternative to man pages
- [tldr](https://github.com/tldr-pages/tldr): user-defined man pages/terminal reference with many client interfaces
- [pet](https://github.com/knqyf263): a terminal-based snippet manager
- [dash](https://kapeli.com/dash): API documentation browser and snippet manager