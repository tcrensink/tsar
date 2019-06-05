"""
Currently testing/verifying elasticsearch I/O
example: https://elasticsearch-py.readthedocs.io/en/master/#example-usage

- start elastic search server, get client (launch_elasticsearch)
- generate json docs from wiki pages 
- add docs to index

"""
import os
import subprocess
import yaml
from uuid import uuid4
from tsar.lib import search, parse
WIKI_PATH = '/Users/trensink/git/my_repos/tsar/wiki_documents'
DOC_PATH = os.path.join(WIKI_PATH, 'test2.md')
CONFIG_PATH = './config.yaml'
EXTENSIONS = ['.md']
INDEX = 'wiki'
DOC_TYPES = ['wiki_page']


PROMPT = """
Please choose one of the following:
<enter query string>: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax>
'+' add file to index
'e' to edit a file (in sublime text)
'-' remove file from index
'q' quit
"""

if __name__ == '__main__':

    print('starting elasticsearch...')
    response = search.launch_es_daemon()
    print('creating client...')
    es = search.es_client()
    print('generating elasticsearch documents from wiki markdown pages...')
    docs = parse.gen_docs(WIKI_PATH, parser=parse.wiki_page, extension='.md')
    print('indexing docs in elasticsearch index="wiki"...')
    for doc in docs:
        es.index(index=INDEX, doc_type='wiki_page', body=doc[1], id=doc[0])

    print('getting editor...')
    with open(CONFIG_PATH) as fp:
        editor_dict = yaml.load(fp)
    editor_cmd = editor_dict['editor']

    while True:
        es.indices.refresh(index="wiki")
        input_str = input(PROMPT)
        if input_str == 'q':
            print('goodbye!')
            break
        if input_str == '+':
            body_str = input('enter body of new record:\n')
            uuid = uuid4().hex
            es.index(index=INDEX, doc_type='wiki_page', body=body_str)
            print('document added at {}'.format(uuid))
        if input_str == '-':
            id_str = input('enter id of document to delete:\n')
            es.delete(index='wiki', doc_type='wiki_page', id=id_str)
        if input_str == 'e':
            while True:
                record_path = input('enter id of documnt to edit:\n')
                if es.exists('wiki', id=record_path):
                    subprocess.Popen('{} -w {}'.format(editor_cmd, record_path), shell=True).wait()
                    print('updating record...')
                    body = parse.wiki_page(record_path)
                    # body = json.loads(body)
                    # body = dict(doc:body)
                    # body['doc'] = body.pop('body')
                    es.index(index=INDEX, doc_type='wiki_page', id=record_path, body=body)
                    break
                if record_path == 'q':
                    break
                else:
                    print('record doesn\'t exist; try again (or press "q")')
        else:
            results = es.search(q=input_str)
            df = search.results_to_df(results)
            print('\n\n\n***RESULTS***:\n\n{}'.format(df))


