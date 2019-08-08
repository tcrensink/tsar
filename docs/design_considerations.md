#V2
This page outlines TSAR's functionality, utility, and distinction from similar existing tools.

# WHAT IS TSAR?
- A tool to aid in *frictionless* interaction with unruly data.  TSAR generates metadata for a collection of records and provides a set of tools for finding relevant information quickly.  Examples:
    - you have a catelog of files, and you want to know what's in them.  TSAR generates metadata for each file on the fly and allows you to search for keywords.
    - you wish to be sharp for an interview or test. You have collected the information, but need a method for reviewing so that you remember it when needed; TSAR provides spaced-repetition functionality for all information you eventually wish to absorb in your brain.
    - you want to maintain a Personal Knowledge Repo: you want access to information you've previously recorded even when it is difficult to recall where you've put it; further more, you want to auto-associate each file with others like it for later browsing.  This is the grand vision of TSAR.


# USECASES
0. **Semantic key-value store** - return specific information value provided a semantic key:
    I have a specific task I wish to accomplish (key) and know that specific information exists to accomplish this task (value).  I don't care to remember the information in detail - I simply want to recall/reproduce it as quickly as possible by providing the key.  Example: add a folder to a conda environment (semantic key): `conda develop -n your_env .` (value)

1. **Learning Aid** - aid information ingestion into your brain:
    I am learning stats.  As I read through a book, it is useful to log what I've read for later review, or record my own insights for later reference.  Two specific features are useful here:
    - a "diary" of what I've learned that can be recalled quickly on command
    - a (anki-like) review feature that suggests whe to look over old material so it gradually seeps into my memory

2. **Idea Capture and Reminder** - remind yourself of a previous thought that is worth revisiting:
    This is capture/reminder, or virtual sticky notes.  You have a thought you'd like to revisit - a note, or bout of inspiration, and you want to capture it before it floats away.  Here you need a prompt to revisit the information, rather than simply retrieve it as needed; it is distinct from the Semantic key-value store in this way.  Examples: 1) Don't forget to pay rent in three days! or, 2) here's your journal template for the day, and a review of last week/quarter/decade

3. **Browse Related Information**: map relatedness of your thoughts
    Example: I studied Random Forests last year, and want to conjure related tasks (e.g., binary classification metrics).  Can you present/organize information to be browsed by "adjacent" semantic meaning?

4. **Introspection of (previously unseen, digital) information**: what is in this folder?
    You are provided with (digital) information of unknown contents (e.g. github repo) and you wish to introspect it to gain understanding.  For this task, search and browse functionality is key.

# Key value add
- The *fastest* interface from thought to information retrieval.  Google/Stack Overflow set par here.
- The *fastest/easiest* method for capture/adding new data.  If it takes too much time to add an example while you work, it's useless.  Maybe two tier system (add information, refine information?)
- The *fastest* way to organize for later retrieval.  Compare with wiki/manually generated relational graph... too slow!
- Extensible and flexible: Tsar now is a managed metadata layer on top of source files.  You can define a new *record_type* and completely change how source files are parsed and how they are stored.


# Information accessibility and interface properties
- search: you provide some relatively unique partial content or metadata (time, tag, etc.) and return all matching records.

- browse by semantic similarity: you don't have identifying information for the record you seek, but recall the semantic content.  Provided a list of records, you would be able to determine which records are most related.  TSAR should implement a method for "crawling" a semantic similarity graph to the correct record

- filter: you are certain you have criteria that includes the record you desire, but also contains too many other records.  Iterative filtering or "subtractive querying" is useful for removing undesired records.

- discoverability: there should be contextual hints at the scope and general terrain of records 1) in some semantic vicinity and 2) globally in the database.  This may be some combination of factors, including (but not limited to) a total record count, netword (or other) visualization of the full records, and browsing metadata.


# Desired features and use cases
- (primary) search, browse, filter
- (primary) fast keyboard-only access for search, browse, add record functionality
- (primary) semi-automated meta data generation (date, suggested tags), indexing, and semantic indexing (browsing)
- (secondary) dairy/log tooling: specific (but definable) formatting for tracking processes through time
- (secondary) memory integration tools: spaced repetition, review mode
- (secondary) snippet manager tools: clipboard integration, syntax highlighting, etc.
- (optional) Local explore: provide search, browse functionality for a given folder


# What are the most similar tools that exist, and how is TSAR better?
I already use X; why should I use TSAR?

Google/bookmarked browser: TSAR is a tool for self-generated/managed information, not the entire internet.  You can therefore access more relevant (even personal) information, and curate what informatino is stored/retrieved by defining `record_types`.

Stack Overflow: TSAR is more general than a snippet manager.  That being said, Stack overflow is a great resource, and hard to beat for finding relevant, vetted code quickly.  Consider making a stack_overflow `record_type` and pulling from the API...  if so, the command line interface might even be faster than opening the browser.

Local wiki: TSAR's command-line access should be faster and break developer workflow less than booting a browser-based wiki, and is not coupled to internet browsing windows.

Local DB (postgres, pandas, etc): the basic funtionality of TSAR could be achieved with a very thin wrapper around a command-line database utility (e.g., psql).  Distinct from performance of search, TSAR provides a faster user experience for the specific task it's designed to do (add new records, retrieve old ones).

Local files + grep: this is in some ways a "poor man's" TSAR.  TSAR aims to improve on this with expanded functionality, human friendly syntax, and iteractive features that iteratively allow you to retrieve information faster than successive grep searches.


# Data retrieval
- **search**: fuzzy search of multiple fields, set operations, maybe a "smart ranking" system
- **tagging**: labels for filtering relevance, live update


# Storage and representation (see technical outline for more)
- **spatial storage representation**
	- 3D spatial location is strongly associated with memory; top method used by memorization masters.
	- 3 dimensions is incapable of representing the multifold connection between concepts and ideas, so it may only be loosely relational, or at least not static

- **temporal storage representation**
	- every recorded/tagged (stored) by date (for example, the wiki).
	- naturally unique; there is only one time/day associated with a page you create...
