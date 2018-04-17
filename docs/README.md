# tsar is...
- snippet-based information managment system  
- editable, searchable, and browsable
- encourages storing information as examples rather than specifications
- a key component of a broader personal knowledge management system

# How is it different/better than other snippet managers or information management tools?
- tsar is designed to be an extension of your memory.  Specifically, the interface is designed to be the *fastest* method of storing and retrieving information in a terminal environment, erasing the barrier between thought and digitally stored information.

# Key features
- Examples are indexed and represented as an association network; tsar supports query-based search and association based browsing.
- search: 	As you type.  Concise and simple syntax includes wildcard, union, and intersection operations
- browse: 	Crawl the auto-generated knowledge association network to find related information
- tags:		Label based organization

# Feature wishlist
- a browsing function: automate an underlying association network of examples
- optimized search through meta information: date added, previous search/result pairs, etc.
- syntax highlighting
- (live) suggested tags, ala stack overflow
- variable insertion for code snippets
- automatically store current example to clipboard (save prior cb contents, auto update with example)
- meta data: distinguish between knowledge very well known, those currently in process, and those deferred.
- visualizations of usage statistics: successful searches, distr. of example usage, examples never accessed, etc.
- stackoverflow API plugin
- memory retention tools: bring up examples that haven't been looked at in a while
- export to file format useful for other search tools, e.g. grep/finder
- shared example files via github
- X realtime search
- X fuzzy/stem search

# Key considerations
- What is the *fastest* interface from thought to example?  If it's not faster than Google/Stack Overflow, you fail.
- What is the *fastest/easiest* method for capture/adding new data?  If it takes too much time to add an example while you work, it's useless.  Maybe two tier system (add information, refine information?)
- What is the *fastest* way to organize for later retrieval? Compare with wiki/manually generated relational graph... too slow!

# Data retrieval
- **search**: fuzzy search of multiple fields, set operations, maybe a "smart ranking" system
- **tagging**: labels for filtering relevance, live update

# Storage/organization ideas
- **database with fields**: name, date (timestamp index?), description, tags.
- **metadata**: access, edit, search histories

- **spatial storage representation**
	- 3D spatial location is strongly associated with memory; top method used by memorization masters.
	- 3 dimensions is incapable of representing the multifold connection between concepts and ideas, so it may only be loosely relational, or at least not static

- **temporal storage representation**
	- every recorded/tagged (stored) by date (for example, the wiki).
	- naturally unique; there is only one time/day associated with a page you create...

# Similar projects and inspiration
- bro pages
- https://github.com/bluenote10/PandasDataFrameGUI
- [search tool](http://www.voidtools.com/)
- http://marcusvorwaller.com/blog/2015/12/14/personal-knowledgebases/
- [octotagger](https://github.com/TeamOctoTagger/OctoTagger)
- [pet](https://github.com/knqyf263)
- dash (realtime filter, great GUI/keyboard access)
- thoughts on tagging: https://stackoverflow.com/questions/334183/what-is-the-most-efficient-way-to-store-tags-in-a-database
