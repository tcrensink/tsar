You can "boost" term importance at query time using a caret operator: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_boosting

Examples:
`query boost^4`

`query^0.5 boost`
