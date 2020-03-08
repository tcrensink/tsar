Phrase queries allow word-distance flexibility; that is the words may be separated by some distance in the text and still match: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-fuzziness

Example:
"distance separated"~4