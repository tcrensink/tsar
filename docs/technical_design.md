# Design
The following represent composable pieces of TSAR, modular enough that they could be redesigned/rebuilt with minimal interference with the other pieces.  This is a loose API specification of what is ingested and returned from each section:


# DATA
Each "tsar database" is a collection of markdown files and associated metadata files.  These are preferable as they are human readable and editable, and leaves your data in a usable format in the event that you'd like to keep it but no longer use TSAR.
IO: record content added from user.  Metadata (semi) auto generated, including date, tags, usage history.

**DB**:
init:
- path
attr:
- db_path, records (paths; includes metadata), name, creation_date, timestamp_last_edit
meth:
- add record
- remove record
- edit record
- refresh_records (looks for paths again)

# SEARCH
First implementation: elasticsearch

Given a database, generates an index that is searchable from some specific search syntax.  The data is unmodified in this process, and differing search engines can be implemented with little difficulty.  
**SEARCHER**
init: 
- DB, engine_name, index, query
attr:
- query, index, results (managed attr?), history (query, search, results)
meth:
- reindex
- update_results (? results should probably be managed to reflect query...)
- undo (pulls up previous q,s,r in history)
- redo (goes to next q,s,r in history)

(cache index, results?)


# BROWSE
First implementation: SpaCy.  Possible tools: NetworkX

Based on database, generate a semantic network: https://en.wikipedia.org/wiki/Semantic_network.  
**BROWSER**
init: 
- DB, network_generator_name, network, selected_record
attr:
- records_ranking (managed on selected_record)
- selected record: (pulled from app)
meth:
- ?


# APP
Python 3.X

Given all the components above, collect them into a cohesive container that manages everything under the hood, as well as the Screen object that handles the visual interface (below).  This houses the "current state" of all the components.
**APP**:
init:
- DB, Searcher, Browser, selected_record, screen_state
attr:
- history: list of [{ts:timestamp, query:query, results:results, selected_record:sr, related_records:related_records}
- DB
- Searcher
- Browser
- Selected record

meth:
- update_state_from_Screen (returns kwarg information from the Screen that is passed onto the App and contained objects)
- update_DB (updates records, based on kwarg input)
- update_Searcher (updates search object based on app state)
- update_Broswer (updates browser object based on app state)
- update_selected_record (modifies )
- map_keys (from yaml file definition?)
- close


# SCREEN
First implementation: urwid.  Possible tools: 

This handles visual display, and critically passage of user input data to the app (and contained objects).  This interface is the hardest part to handle.

init: screen_state (dictates what is rendered)
attr: widgets...
meth:
- update screen (?)
- update_results_display
- update_query_display
- update_selected_record_display



