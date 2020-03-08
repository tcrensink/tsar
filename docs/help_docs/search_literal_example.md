Exact string matches can be enforced with quotes.  Note that reserved characters: `+ - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /` must be escaped with backslash: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#_reserved_characters

Example
`content:"Exact string"`

`content:\(here\)` -> searches for "(here)" character
