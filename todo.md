# V2: start with very fast, lightweight experiments on UI, UX
# Resume test_script.py
X install elasticsearch
X write elasticsearch example:
    X generate document (string repr of json)
    X index document
    X search for document
    X retrieve document in full
X write elasticsearch example to query local markdown
    X walk path from base folder
    X generate docs for each file
    X add docs to elasticsearch index with client

- (draft) write repl to query records, sanity check elasticsearch
    - prompt for query
    - display results names
    - result prompt to requery or display contents

- (draft) add record in terminal from editor
    - define editor excutable in config file
    - run "tsar record_name" (generates new record)
    
#   USECASES

0. **Semantic key-value store**: return specific information value provided a semantic key
    I have a specific task I wish to accomplish (key) and know that specific information exists to accomplish this task (value).  I don't care to remember the information in detail - I simply want to recall/reproduce it as quickly as possible by providing the key.  Example: add a folder to a conda environment (semantic key): `conda develop -n your_env .` (value)

1. **Learning Aid**: aid information ingestion into your brain
    I am learning stats.  As I read through a book, it is useful to log what I've read for later review, or record my own insights for later reference.  Two specific features are useful here: 
    - a "diary" of what I've learned that can be recalled quickly on command
    - a (anki-like) review feature that suggests whe to look over old material so it gradually seeps into my memory 

2. **Idea Capture and Reminder**: remind yourself of a previous thought that is worth revisiting
    Inspiration strikes, and you want to catch it before it floats away.  Later, you need to be prompted to resume this train of thought - it is distinct from the Semantic key-value store in this way; you want fast access to "paper" and a prompt to revisit the thought.  Example: a mathematical idea that might be fruitful

3. **Information Exploration**: map relatedness of your thoughts
    Example: I studied Random Forests last year, and want to conjure related tasks (e.g., binary classification metrics).  Can you present/organize information to be browsed by "adjacent" semantic meaning? 

4. **Introspection of (previously unseen) information**: what is in this folder?
    You are provided with (digital) information of unknown contents (e.g. github repo) and you wish to introspect it to gain understanding.  For this task, search functionality is key.
 
