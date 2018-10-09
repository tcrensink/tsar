"""
the current contents of the screen.  This is an MVP example, that includes only:

- live search bar
- live results
- results can be selected; contents displayed below
"""

class Screen(object):
    """
    contains tsar.Search object
    responsible for 
    """
    def __init__(self):
        self.search = tsar.Search()

    def update_selection(self):
        """
        update 
        """

    def show_results(self):
        pass

    def update_query(self, query):
        """
        change the query
        """
        self.search.query = query
