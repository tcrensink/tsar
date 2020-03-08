By default the following is true of space separated search terms: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_boolean_operators

- All search fields are searched
- Space separated terms are treated independently
- Term order does not affect results
- It is *not* required that each term is matched for a "hit"
