"""
Currently testing/verifying elasticsearch I/O
example: https://elasticsearch-py.readthedocs.io/en/master/#example-usage

- start elastic search server, get client (launch_elasticsearch)
- generate json docs from wiki pages 
- add docs to index

"""
import os
from tsar.lib import search, parse
WIKI_PATH = '/Users/trensink/git/my_repos/tsar/wiki_documents'
DOC_PATH = os.path.join(WIKI_PATH, 'test2.md')
EXTENSIONS = ['.md']
INDEX = 'wiki'
DOC_TYPES = ['wiki_page']

if __name__ == '__main__':

    print('starting elasticsearch...')
    response = search.launch_es_daemon()
    print('creating client...')
    es = search.es_client()
    print('generating elasticsearch documents from wiki markdown pages...')
    docs = parse.gen_docs(WIKI_PATH, parser=parse.wiki_page, extension='.md')
    print('indexing docs in elasticsearch index="wiki"...')
    for doc in docs:
        es.index(index=INDEX, doc_type='wiki_page', body=doc)
    res = es.search(index="wiki", body=dict(query=dict(match_all=dict())))
    print('showing all added documents: {}'.format(res))
    

