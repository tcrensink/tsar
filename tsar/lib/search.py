#! /Users/trensink/anaconda3/bin/python
"""
syntax: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax
docs: https://elasticsearch-py.readthedocs.io/en/master/
"""
from elasticsearch import Elasticsearch
import pandas as pd
import requests
import os
import subprocess
from tsar import MODULE_PATH, REPO_PATH
from tsar.lib import parse
from pandas.io.json import json_normalize

# elastic search uses 9200 by default
HOST = 'localhost'
PORT = 9200
ELASTICSEARCH_EXEC_PATH = os.path.join(REPO_PATH, 'dependencies', 'elasticsearch-7.1.1/bin/elasticsearch')
SERVER_FILE = os.path.join(REPO_PATH, 'server.txt')


def launch_es_daemon(
    target=ELASTICSEARCH_EXEC_PATH,
    server_file=SERVER_FILE,
    host=HOST,
    port=PORT,
    ):
    """Start the elasticsearch server, verify response, return a client

    Todo:
        - check for running instance of daemon/server (process_info.return_code == 1 when alrady running)
    """
    # start elasticsearch daemon, record pid in meta_data file:
    cmd = "{} -d -p {}".format(target, server_file)
    result = subprocess.run(cmd, shell=True)
    test_server(host=HOST, port=PORT, verbose=True)
    return result


def shutdown_es_daemon():
    """safely shut down daemon.
    - read pid
    - kill pid
    - clean up file
    """
    pass


def test_server(host=HOST, port=PORT, verbose=True):
    """test elasticsearch server response
    """
    response = requests.get('http://{}:{}'.format(host, port))
    status_code = response.status_code
    if verbose:
        if status_code == 200:
            print('server connection succssful')
        else:
            print('server error, status code {}'.format(status_code))
    return response


def es_client(host=HOST, port=PORT):
    """
    return elasticsearch client
    """
    print('returning elasticsearch client')
    es_client = Elasticsearch([{'host': HOST, 'port': port}])
    return es_client


def list_indices(client):
    """show all indices (indexes) available to the server
    """
    indices = client.indices.get_alias("*")
    return indices


def results_to_df(results_dict):
    """
    """
    df = json_normalize(results_dict['hits']['hits'], sep='_')
    names = {name:name.strip('_') for name in df.columns}
    df.rename(columns=names, inplace=True)
    return df



