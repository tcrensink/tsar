# tsar is...
- an editable Repository Of Simple Examples (snippet manager): because examples are more useful than documentation
- an extension of your working memory: the fastest connection between a thought and working example

# How is it better than Dash, nvalt, other snippet managers?
- tsar is designed to be the *fastest* path from your thought to example code.  It is designed to be an extension of your working memory.  Specifically:
- accessible from... (terminal, or python shell?)
- live search update
- successive search filters
- simple and intuitive search syntax

# Key features
- search
- tags
- sorting, union/intersection filters


# Feature wishlist
- fuzzy, realtime search
- suggested tags
- accessible at a keystroke (GUI? terminal? python shell?)
- variable insertion (dash)
- copy to clipboard/cursor location
- enhance/refine search/example connection with clustering algos: as a start, capture if search yielded sought useful examples
- distinguish between knowledge very well known, those currently in process, and those deferred.  Key metric: time spent looking at example/length in lines
- suggest related examples when viewing one
- visualizations of usage statistics: successful searches, distr. of example usage, examples never accessed, etc.
- memory retention tools: bring up examples that haven't been looked at in a while
- file format useful for other search tools, e.g. grep/finder
- shared example files via github


# Similar projects and inspiration
- bro pages
- https://github.com/bluenote10/PandasDataFrameGUI
- [search tool](http://www.voidtools.com/)
- http://marcusvorwaller.com/blog/2015/12/14/personal-knowledgebases/
- [octotagger](https://github.com/TeamOctoTagger/OctoTagger)
- [pet](https://github.com/knqyf263)
- dash (realtime filter, great GUI/keyboard access)
- thoughts on tagging: https://stackoverflow.com/questions/334183/what-is-the-most-efficient-way-to-store-tags-in-a-database
- nvalt

# Repo organization
- `/tsar` 		: python package (put on PYTHONPATH)
- `/tsar/data` 	: auxiliary data needed for examples
- `/tsar_files` : example files 


