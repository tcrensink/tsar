# COLLECTION QUERY WINDOW `ctrl-s`

Each collection parses source documents into metadata records.  Fields can be queried to locate the original source documents using the lucene query syntax, https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax.

Example queries are shown below for a collection of arxiv records with the following fields:
(access_times, authors, content, keywords, publish_date, title)


# QUERY EXAMPLES

- `reinforcement`                               search all fields for `reinforcement` (by default)
- `title:reinforcement`                         search `title` field for "reinforcement"
- `title:"reinforcement learning"`              search `title` field for "reinforcement learning"
- `reinforc*`                                   search all fields with wildcard completion
- `reinforcemnt~2`                              search with fuzzy matching (Damerau-Levenshtein edit distance of 2 or less)
- `"deep learning"~3`                           search with word distance 3 or less (e.g. `deep reinforcement learning`)
- `publish_date:[2018-01-01 TO 2020-12-31]`     search `publish_date` from 2018 to 2020 
- `publish_date:[2015-01-01 TO *]`              search `publish_date` 2015 and later
- `deep^2 "reinforcemnt learning"`              search both terms, boosting relevance of "deep" 
- `deep^0.5 "reinforcemnt learning"`            search both terms, reducing relevance of "deep" 
- `-deep +"reinforcement learning"`             search excluding "deep", requiring "reinforcement learning" 
- `title:("RL" OR "reinforcement learning")`    search title for either string 


# NOTES
- multiple terms, unquoted, are interpreted as `OR` by default: 
  - `deep learning` -> `deep OR learning`
- booleans operators have two representations: `AND` `OR`, `&&` `||`


- reserved characters: `+ - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /`
  - are escaped with a slash `\+`
  - `<` and `>` cannot be escaped
