"""
Elasticsearch server, client classes.
"""
import subprocess
import os
import requests
import pandas as pd
from requests.exceptions import ConnectionError, HTTPError
from pandas.io.json import json_normalize
from tsar import MODULE_PATH, REPO_PATH
from urllib.parse import quote_plus, unquote_plus
from tsar.config import ELASTICSEARCH_PORT

HOST = "localhost"
BASE_URL = f"http://{HOST}:{ELASTICSEARCH_PORT}"

ELASTICSEARCH_PATH = "/usr/local/bin/elasticsearch"
SERVER_FILE = os.path.join(REPO_PATH, "server.txt")


def encode_url_str(raw_url_string):
    """Standard substitutions for url strings.

    see: https://en.wikipedia.org/wiki/Percent-encoding
    """
    quoted_url_string = quote_plus(raw_url_string)
    return quoted_url_string


class Server(object):
    """ElasticSearch server class.

    methods to add:
    - n documents in index: /index/_count
    """

    def __init__(self, es_app=ELASTICSEARCH_PATH, server_file=SERVER_FILE):
        self.app = es_app
        self.server_file = server_file

    def start(self):
        """Start elasticsearch server if not running."""
        client = Client()
        if client.test_connection():
            return
        else:
            cmd = f"{self.app} -d -p {self.server_file}"
            _ = subprocess.call(cmd.split(" "))
            while True:
                res = Client().test_connection()
                if res:
                    return

    def shutdown(self):
        """shutdown service."""
        raise NotImplementedError()

    def status(self):
        """Status of server."""
        raise NotImplementedError()


class Client(object):
    """Elasticsearch client used by tsar, uses rest API."""

    def __init__(self, host=HOST, port=ELASTICSEARCH_PORT):
        self.session = requests.Session()
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    @property
    def return_indexes_summary_df(self):
        res = self.session.get(self.base_url + "/_cat/indices?v")
        res.raise_for_status()
        table_values = [j.split() for j in res.text.splitlines()]
        columns = table_values[0][:]
        data = table_values[1::]
        df = pd.DataFrame(data=data, columns=columns)
        return df

    def index_record(self, record_id, record_index, collection_name):
        """Index a record.

        Requires search-index entry given by RecordDef.gen_record_index sans record_id
        """
        encoded_id = encode_url_str(record_id)
        url = f"{self.base_url}/{collection_name}/_doc/{encoded_id}"
        res = self.session.put(url, json=record_index)
        res.raise_for_status()
        return res

    def return_record_index(self, record_id, collection_name):
        """Return dict of index values for record_id."""
        encoded_id = encode_url_str(record_id)
        url = f"{self.base_url}/{collection_name}/_doc/{encoded_id}"
        res = self.session.get(url)
        res.raise_for_status()
        return res

    def index_records(self, record_ids, record_indexes, collection_name):
        """Index a list of records.

        Optimize with bulk api:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
        """
        for r_id, r_ind in zip(record_ids, record_indexes):
            self.index_record(
                record_id=r_id, record_index=r_ind, collection_name=collection_name
            )

    def delete_record(self, record_id, collection_name):
        """Remove record from index."""
        encoded_id = encode_url_str(record_id)
        url = f"{self.base_url}/{collection_name}/_doc/{encoded_id}"
        res = self.session.delete(url)
        res.raise_for_status()
        return res

    def query(
        self, collection_name, query_str="*", default_fields="*", num_results=12,
    ):
        """Basic query using the lucene search syntax.

        Discussion of GET request with a body:
        https://www.elastic.co/guide/en/elasticsearch/guide/current/_empty_search.html
        """
        url = f"{self.base_url}/{collection_name}/_search"
        json_params = {
            "query": {
                "query_string": {
                    "query": query_str,
                    "default_field": default_fields,
                    "analyze_wildcard": "true",
                },
            },
            "size": str(num_results),
        }
        try:
            res = self.session.get(url, json=json_params)
            results = res.json()
        except HTTPError:
            res = None
        return results

    def new_index(
        self, collection_name, mapping,
    ):
        """Crate elasticsearch index by name."""
        url = f"{self.base_url}/{collection_name}"
        res = self.session.put(url, json=mapping)
        res.raise_for_status()
        return res

    def drop_index(
        self, collection_name,
    ):
        """Delete an index by name."""
        url = f"{self.base_url}/{collection_name}"
        res = self.session.delete(url)
        res.raise_for_status()
        return res

    def return_index(self, collection_name):
        """Return index info for collection."""
        url = f"{self.base_url}/{collection_name}?pretty"
        res = self.session.get(url)
        res.raise_for_status()
        return res

    def return_mapping(self, collection_name):
        """Return index mapping for collection."""
        res = self.session.get(self.base_url + f"/{collection_name}/_mapping/?pretty")
        mapping = res.json()
        return mapping

    def return_fields(self, collection_name):
        """Return fields, types for an index.

        Use pd.DataFrame.from_dict(properties)
        """
        mapping = self.return_mapping(collection_name=collection_name)
        # extract fields, types from mapping:
        properties = mapping[collection_name]["mappings"]["properties"]
        return properties

    def test_connection(self):
        """Test connection with elasticsearch server."""
        try:
            res = self.session.get(self.base_url)
            res.raise_for_status()
            connection_status = True
        except ConnectionError:
            connection_status = False
        return connection_status
