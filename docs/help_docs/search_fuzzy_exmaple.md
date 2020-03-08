Fuzzy search uses the Levenshtein edit distance.  Specify the number of single character typos, transpositions, or omissions allowable for a match.  Default value is 2 for `~` : https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-fuzziness

Example:

`Levenhsteik~` -> matches Levenshtein
