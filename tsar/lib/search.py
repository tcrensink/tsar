"""
Elasticsearch server, client classes.
"""
import subprocess
import time
import os
import requests
import pandas as pd
from requests.exceptions import ConnectionError, HTTPError
from pandas.io.json import json_normalize
from tsar import MODULE_PATH, REPO_PATH
from urllib.parse import quote_plus, unquote_plus

ELASTICSEARCH_PORT = 8138
HOST = "localhost"
BASE_URL = f"http://{HOST}:{ELASTICSEARCH_PORT}"

ELASTICSEARCH_PATH = "/usr/local/bin/elasticsearch"
SERVER_FILE = os.path.join(REPO_PATH, "server.txt")


def return_index_name(collection_name, doc_type_str, sep="__"):
    """Return formatted index string"""
    index_name = f"{collection_name}{sep}{doc_type_str}".lower()
    return index_name


def encode_url_str(raw_url_string):
    """Standard substitutions for url strings.

    see: https://en.wikipedia.org/wiki/Percent-encoding
    """
    quoted_url_string = quote_plus(raw_url_string)
    return quoted_url_string


class Server(object):
    """ElasticSearch Server. """

    def __init__(
        self, server_file=SERVER_FILE,
    ):
        self.server_file = server_file

    def start(self, timeout=5):
        """Start elasticsearch server if not running.

        timeout is used for when a connection but hasn't finished initializing the indexes.  It would
        be preferable to check the health of the nodes.
        """
        client = Client()
        if client.test_connection():
            return
        else:
            _ = subprocess.run(
                "service elasticsearch start".split(), capture_output=False
            )
            while True:
                res = client.test_connection()
                if res:
                    time.sleep(timeout)
                    return

    def stop(self):
        """shutdown service."""
        _ = subprocess.run("service elasticsearch stop".split(), capture_output=False)

    def status(self):
        """Status of server."""
        _ = subprocess.run("service elasticsearch status".split(), capture_output=False)


class Client(object):
    """Elasticsearch client used by tsar, uses rest API."""

    def __init__(self, host=HOST, port=ELASTICSEARCH_PORT):
        self.session = requests.Session()
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"

    @property
    def summary(self):
        """Return indices summary dataframe."""
        res = self.session.get(self.base_url + "/_cat/indices?v")
        res.raise_for_status()
        table_values = [j.split() for j in res.text.splitlines()]
        columns = table_values[0][:]
        data = table_values[1::]
        df = pd.DataFrame(data=data, columns=columns)
        df = df.set_index("index", drop=True).sort_index()
        return df

    def index_record(self, document_id, record_index, index_name):
        """Index a record.

        Requires search-index entry given by RecordDef.gen_record_index sans record_id
        """
        encoded_id = encode_url_str(document_id)
        url = f"{self.base_url}/{index_name}/_doc/{encoded_id}"
        res = self.session.put(url, json=record_index)
        res.raise_for_status()
        return res

    def return_record_index(self, document_id, collection_name):
        """Return dict of index values for record_id."""
        encoded_id = encode_url_str(document_id)
        url = f"{self.base_url}/{collection_name}/_doc/{encoded_id}"
        res = self.session.get(url)
        res.raise_for_status()
        return res

    def index_records(self, document_ids, document_indexes, collection_name):
        """Index a list of records.

        Optimize with bulk api:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
        """
        for d_id, d_ind in zip(document_ids, document_indexes):
            self.index_record(
                document_id=d_id, document_index=d_ind, collection_name=collection_name
            )

    def delete_record(self, document_id, index_name):
        """Remove record from index."""
        encoded_id = encode_url_str(document_id)
        url = f"{self.base_url}/{index_name}/_doc/{encoded_id}"
        res = self.session.delete(url)
        res.raise_for_status()
        return res

    def query(
        self, index_list, query_str="*", default_fields="*", num_results=20,
    ):
        """Basic query using the lucene search syntax.

        multi-index query:
        https://www.elastic.co/guide/en/elasticsearch/reference/current/multi-index.html

        Using GET request with a body:
        https://www.elastic.co/guide/en/elasticsearch/guide/current/_empty_search.html
        """
        index_str = ",".join(index_list)
        url = f"{self.base_url}/{index_str}/_search"
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

    def new_index(self, index_name, mapping):
        """Crate elasticsearch index by name."""
        url = f"{self.base_url}/{index_name}"
        res = self.session.put(url, json=mapping)
        res.raise_for_status()
        return res

    def drop_index(self, index_name):
        """Delete an index by name."""
        url = f"{self.base_url}/{index_name}"
        res = self.session.delete(url)
        res.raise_for_status()
        return res

    def return_index(self, index_name):
        """Return index info for collection."""
        url = f"{self.base_url}/{index_name}?pretty"
        res = self.session.get(url)
        res.raise_for_status()
        return res

    def index_exists(self, index_name):
        """Return True if index_name exists."""
        url = f"{self.base_url}/{index_name}"
        res = requests.head(url)
        if res.status_code == 200:
            return True
        elif res.status_code == 404:
            return False
        else:
            raise HTTPError(f"response text: {res.text}")

    def rename_index(self, index_name, new_index_name):
        """Rename an index.
        see: https://stackoverflow.com/questions/28626803/how-to-rename-an-index-in-a-cluster
        - make index writable
        - clone original to new
        - delete original
        """
        url_writeable = f"{self.base_url}/{index_name}/_settings"
        self.session.put(
            url=url_writeable, json={"settings": {"index.blocks.write": True,}}
        )

        url_clone = f"{self.base_url}/{index_name}/_clone/{new_index_name}"
        res_clone = self.session.post(
            url=url_clone, json={"settings": {"index.blocks.write": None}}
        )
        url_remove = f"{self.base_url}/{index_name}"
        _ = self.session.delete(url_remove)
        return res_clone

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
