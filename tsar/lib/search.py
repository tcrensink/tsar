#! /Users/trensink/anaconda3/bin/python
"""
syntax: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax
docs: https://elasticsearch-py.readthedocs.io/en/master/

To do:
"""
from elasticsearch import Elasticsearch
from elasticsearch.serializer import JSONSerializer
import numpy as np
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
INDEX = 'wiki'

class TsarEncoder(JSONSerializer):
    """json cannot natively serialize sets; subclass it for TSAR records
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, np.int64):
            return int(obj)

        return JSONSerializer.default(self, obj)


class TsarSearch(object):
    """wrapper around elastic search client for tsar.
    """
    def __init__(self, index=INDEX):
        """
        create a nw tsarsearch instance for index named `index`.

        todo: should this take record_type?
        """
        # launch the es daemon
        self.client = Elasticsearch([{'host': HOST, 'port': PORT}])
        self.index = index

    def delete_index(self):
        """delete current index
        """
        if self.client.indices.exists(self.index):
            self.client.indices.delete(self.index)

    def create_index(self):
        """create an (empty) index
        """
        if not self.client.indices.exists(self.index):
            self.client.indices.create(self.index)

    def _query_records(self, query_str):
        """return raw query results from index.  Top level keys of "results":
        'took',
        'timed_out',
        '_shards',
        'hits'
        """
        results = self.client.search(q=query_str, index=self.index)
        return results

    def query_records(self, query_str, tsar_df):
        """return metadata records matching the query
        """
        raw_results = self._query_records(query_str)
        result_ids = [result['_id'] for result in raw_results['hits']['hits']]

        return result_ids

    def index_record(
        self,
        record,
        record_id,
        record_type,
        encoder=TsarEncoder()
    ):
        """
        - index one record
        - update index for that record
        """
        encoded_record = encoder.dumps(record)
        self.client.index(
            index=self.index,
            doc_type=record_type,
            id=record_id,
            body=encoded_record
        )

    def index_records(self, db_records):
        """update all records to reflect current state of df:

        - delete existing index
        - create new (empty) index
        - index all records in df_records
        - update all records in index
        """
        record_ids = db_records.index.values
        for record_id in record_ids:
            record = db_records.loc[record_id]
            self.index_record(
                record,
                record_id,
                record['record_type'],
                encoder=TsarEncoder()
            )


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


def test_server(host=HOST, port=PORT, verbose=False):
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
    indices = list(client.indices.get_alias("*").keys())
    return indices


def results_to_df(results_dict):
    """
    """
    df = json_normalize(results_dict['hits']['hits'], sep='_')
    names = {name: name.strip('_') for name in df.columns}
    df.rename(columns=names, inplace=True)
    return df


def result_ids(es, query_str=''):
    results_dict = es.search(q=query_str)
    df = results_to_df(results_dict)
    if df.empty:
        ids = []
    else:
        ids = df.id.values
    return ids


def result_preview(es, query_str=''):
    results_dict = es.search(q=query_str)
    df = results_to_df(results_dict)
    if df.empty:
        previews = []
    else:
        previews = df.source_body.values
    return previews
