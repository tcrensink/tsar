"""
this encapsulates the search functionality used in tsar.

This is intended to abstract around the search engine implementation, largely, so that the engine
may be interchanged with minimal interference to tsar.
"""

class Search(object):
    """
    implement the search engine.  Based on the query, return results.  Cache the previous
    search/result pairs?
    """

    def __init__(self, query='*'):
        """
        search has an active query, active results, and the history defined by them
        """
        self.query = query
        self.results = self.update_results(self.query)
        self._search_hist = []
        self._result_hist = []

    def update_results(self, query):
        """
        results of search based on the current query.  This method will change based on
        the search engine used.

        takes: query
        returns: results (dict?)
        """
        

    def _search_hist(self):
        """
        the search history
        """

    def _results_hist(self):
        """
        a store of the result_history
        """
