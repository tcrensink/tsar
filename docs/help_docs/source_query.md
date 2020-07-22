# SOURCE QUERY WINDOW `ctrl-d`

Collections may be associated with a `source`.  Sources can be queried to preview and add more documents to the current collection.  Source queries are specific to the collection type: collections of type `arxiv` will query the arxiv document server while `wiki` collections may take a file path.

# EXAMPLE: PREVIEW, ADD DOCUMENT FROM SOURCE 

1) Select the `help_docs` collection:
  - `ctrl-a` (nav to collections window)
  - press return on `help_docs`

2) Query the associated `source` (folder on computer) for more documents:
  - `ctrl-d` (nav to query source window)
  - type `<path_to_tsar_repo>/tsar/tests/fixtures`, press enter

3) Preview, add document:
  - `shift+right` on selected doc will add to the `help_docs` collection

4) View added document:
  - `ctrl-s` to go to query collection window
  - type `*` to show all records; the added record should be found in this collection
