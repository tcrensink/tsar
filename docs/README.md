<!-- # Screen shots/ Demo -->

# Introducing TSAR: the Textual Storage And Retrieval utility
Tsar is a productivity tool somewhere between a snippet manager and a digital extension of your memory.  It is designed to help you retrieve relevant information snippets *as quickly as possible* from a terminal.  \n\nTsar currently uses search-as-you-type record query; future versions will include sorting, filtering, and record association functionality.  Many additional enhancements are also planned.\n\nSome suggested use cases:\n- a searchable journal/diary\n- a snippet manager for code\n- as a repository of code examples or problem-solution pairs\n- anything else stored as records where fast retrieval of previously stored information is a priority.\n\nTo call tsar from terminal:\n- `$tsar` opens the default database (currently this one, but customizable).  `$tsar db_name` will open a database in `./index_files` corresponding to `./config_files/db_name_config.py`.\n\nPress ENTER to return to the search list and read the records that outline the basic useage of tsar.

# Compatibility and Support
tsar is currently in early Beta, running on macos; Linux support coming soon.

# Installation
To install: download the tsar repository to your computer and run `installation.sh`.

# Getting Started
- call `tsar` with no arguments to open the default databse (currently set to the introduction/tutorial, but customizable).
- Generate a custom database by copying `./config_files/default_config.py` to `./config_files/db_name_config.py`, and call `tsar db_name`.  The first use will generate a database index at `./index_files/db_name`

# How is it different than similar snippet managers or information management tools?
- tsar is designed to be an extension of your memory.  Specifically, the interface is designed to be the *fastest* method of storing and retrieving information in a terminal environment, erasing the barrier between memory recall and terminal-based recall.

# Similar projects and inspiration
- the aim of tsar is to act as a general purpose extension of your memory.  It's intended to get you from: "what was that command/thing/idea/text/thought" to a textual representation as fast as possible, with some (eventual) additional productivity features.  If you like tsar, you may also be interested in:
- bro pages: http://bropages.org
- pandas GUI: https://github.com/bluenote10/PandasDataFrameGUI
- VoidTools Everything: http://www.voidtools.com/
- [octotagger](https://github.com/TeamOctoTagger/OctoTagger)
- [pet](https://github.com/knqyf263)
- dash: https://kapeli.com/dash
