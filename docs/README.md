<!-- # Screen shots/ Demo -->

# TSAR: the Text Storage And Retrieval utility
Tsar is a terminal based snippet manager/database interface to help you store and retrieve information *as quickly as possible*.  Tsar currently uses search-as-you-type query; sort, filter, and browsing records by similarity will be added in the future.

# Compatibility and Support
Tsar is currently in early beta, running on python 3.x for MacOS.  Support for Linux and backward compatibility for python 2.x is planned for future releases.

# Installation
clone this repo and add the executable `tsar` to your path variable.

# Getting Started
The tutorial database walks through basic, operation, and is called without argument:
```bash
$ tsar
```
Createa a new database by copying the default config file, editing, and then calling it as an argument:
```bash
$ cp tsar/config_files/default_config.py tsar/config_files/snippets_config.py
$ tsar snippets
```
restore the tutorial database at any time by deleting `tsar/index_files/default`.  It will be regenerated when you call `tsar` from the command-line.

# Why bother with *another* productivity tool?
Tsar aims to provide the most efficient information storage and retrieval, acting as a digital extension of your memory.  This is achieved via a minimal interface directly in terminal, with powerful recall tools.  A number of peripheral productivity features may be included in future releases as well.  Suggested uses:
- a searchable, taggable general purpose note repository 
- a code snippet or easily forgetten bash command manager
- a daily journal/diary
- anything else where fast storage/retrieval of information from terminal is a priority

# Similar projects
If you like tsar, you may also be interested in similar workflow productivity tools:
- [bro pages](http://bropages.org): the concise, crowd-sourced, example-based alternative to man pages
- [tldr](https://github.com/tldr-pages/tldr): user-defined man pages/terminal reference with many client interfaces
- [pet](https://github.com/knqyf263): a terminal-based snippet manager
- [dash](https://kapeli.com/dash): API documentation browser and snippet manager