#!/usr/bin/env python
"""
This file tests a search-bar TUI frontend with test data (no elasticsearch integration):
https://www.youtube.com/watch?v=hJhZhLg3obk

An example of a BufferControl in a full screen layout that offers auto
completion.
Important is to make sure that there is a `CompletionsMenu` in the layout,
otherwise the completions won't be visible.
"""
import sys
import os
import subprocess
import yaml
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers.sql import SqlLexer
from prompt_toolkit.key_binding import KeyBindings

from tsar import config
from uuid import uuid4
from tsar.lib import search, parse
DOCUMENTS_PATH = '/Users/trensink/git/my_repos/tsar/wiki_documents'
# DOC_PATH = os.path.join(INDEX_PATH, 'test2.md')
# CONFIG_PATH = '../tsar/config.yaml'
EXTENSIONS = ['.md']
INDEX = 'wiki'
DOC_TYPES = ['wiki_page']


PROMPT = """\n
Choose one of the following or enter a search string:
'ls' list documents
'+' add file to index
'e' to edit a file (in sublime text)
'-' remove file from index
'q' quit
"""

def new_doc_path(doc_path=DOCUMENTS_PATH):
    """generate a new (unique) document id
    """
    doc_id = uuid4().hex
    doc_path = os.path.join(doc_path, doc_id)
    return doc_path


def gen_key_bindings():

    bindings = KeyBindings()
    @bindings.add('c-x')
    def _(event):
        " Exit when `c-x` is pressed. "
        event.app.exit()

    @bindings.add('a')
    def _(event):
        # action:
        print('testing action...')

    @bindings.add('q')
    def _(event):
        " Exit when `q` is pressed. "
        event.app.exit()

    @bindings.add('down')
    def _(event):
        # move focus to next window
        pass
    @bindings.add('up')
    def _(event):
        # move focus to next window
        pass
    return bindings

def initialize_search(documents_path=DOCUMENTS_PATH):
    print('starting elasticsearch...')
    response = search.launch_es_daemon()
    print('creating client...')
    es = search.es_client()
    print('generating elasticsearch documents from wiki markdown pages...')
    es_docs = parse.gen_docs(documents_path, parser=parse.wiki_page, extension='.md')
    print('indexing docs in elasticsearch index="wiki"...')
    for doc in es_docs:
        es.index(index=INDEX, doc_type='wiki_page', body=doc[1], id=doc[0])
    return es

if __name__ == '__main__':

    print('getting default programs...')
    # with open(CONFIG_PATH) as fp:
    #     editor_dict = yaml.safe_load(fp)
    # editor_cmd = editor_dict['editor']
    editor_cmd = config.EDITOR
    es = initialize_search()
    bindings = gen_key_bindings()
    session = PromptSession()

    while True:
        es.indices.refresh(index="wiki")

        try:
            input_str = session.prompt('query: ', key_bindings=bindings)
        except KeyboardInterrupt:
            break  # Control-C pressed.
        except EOFError:
            break  # Control-D pressed.

        if input_str == 'ls':
            print('listing all existing documents:')
            search.display_results(query_str='*')
            continue
        if input_str == '+':
            print('add new document...')
            # body_str = input('enter body of new record:\n')
            doc_path = new_doc_path()
            subprocess.Popen('{} -w {}'.format(editor_cmd, doc_path), shell=True).wait()
            body = parse.wiki_page(doc_path)
            es.index(index=INDEX, doc_type='wiki_page', body=body, id=doc_path)
            print('document added at {}'.format(doc_path))
            continue
        if input_str == '-':
            display_results(query_str='*')
            id_str = input('enter id of document to delete:\n')
            es.delete(index='wiki', doc_type='wiki_page', id=id_str)
            continue
        if input_str == 'e':
            doc_path = input('enter id of document to edit:\n')
            if es.exists('wiki', id=doc_path):
                print('updating record...')
                subprocess.Popen('{} -w {}'.format(editor_cmd, doc_path), shell=True).wait()
                body = parse.wiki_page(doc_path)
                es.index(index=INDEX, doc_type='wiki_page', id=doc_path, body=body)
                print('document revised.')
                continue
            else:
                print('record doesn\'t exist')
        else:
            results = es.search(q=input_str)
            df = search.results_to_df(results)
            print('\n\n\n***RESULTS***:\n\n{}'.format(df))



if __name__ == '__main__':

    main()