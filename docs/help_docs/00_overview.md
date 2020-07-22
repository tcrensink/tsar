# Overview:
tsar data is organized into document `collections` that are viewed via windows described below.  Each collection is associated with a `record definition` that defines the behavior on a user interaction (e.g., the app that a document is opened in). 


## COLLECTION SELECT WINDOW `ctrl-a`
Choose an active collection that is accessed in other windows.  Help docs are provided as a default collection.

## COLLECTION QUERY WINDOW `ctrl-s`
Query records in a collection using Lucene Query Syntax (see other docs for examples).  Press `return` to open doc.

## SOURCE QUERY WINDOW `ctrl-d`
If a `source` is associated with the collection (e.g. ArXiv or filesystem), query for additional records. 
`shift + right` adds selected documents to collection.  Query syntax is specific to the collection/source.

## ADDITIONAL SHORTCUTS
- disconnect `ctrl-q`
- shut down `ctrl-c`

## TERMINAL COMMANDS
- reconnect to tsar: `tsar`
- restart tsar: `docker kill tsar && tsar`
