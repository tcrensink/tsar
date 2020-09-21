"""This module contains:
- DataBase class:   handles storage addition/removal of records
- Collection class: high level interface for attribute objects DataBase, Client, Browser, RecordDef, etc.

- Lookup functions to find associated RecordDef
"""
import os
import pandas as pd
from tsar import COLLECTIONS_FOLDER, HOST_REPO_PATH
from tsar.config import DEFAULT_COLLECTION
from tsar.lib import search
from tsar.lib.record_def import RecordDef
from tsar.lib import ssh_utils

# must be imported to be recognized as subclasses...
from tsar.lib.record_defs.wiki_record import WikiRecord
from tsar.lib.record_defs.arxiv_def import ArxivRecord
from tsar.lib.record_defs.omni_record import OmniRecord
import datetime
from requests import HTTPError

# df that contains summary info for all collections
DB_META_PATH = os.path.join(COLLECTIONS_FOLDER, "collections_db.pkl")
META_DB_COLS = ["record_type", "creation_date"]


def gen_default_collection(
    collection_name=DEFAULT_COLLECTION, 
    record_def=WikiRecord,
    default_source=os.path.join(HOST_REPO_PATH, "docs/help_docs"),
):
    default_coll = Collection.new(collection_name=collection_name, RecordDef=record_def)
    records = default_coll.query_source(default_source)
    for record in records:
        default_coll.add_record(record)


class Data(object):
    """Class that contains collection records, meta data."""

    def __init__(self, collection, folder):
        self.db_path = self.return_db_path(collection, folder=folder)
        self.df = pd.read_pickle(self.db_path)

    @classmethod
    def new(cls, collection_name, RecordDef, folder):
        """Create dbs associated with collection before instantiating object.

        """
        db_path = cls.return_db_path(collection_name, folder=folder)
        db_folder = os.path.dirname(db_path)

        # create folders as needed, empty df
        if not os.path.exists(db_path):
            os.makedirs(db_folder) if not os.path.exists(db_folder) else None
            df = pd.DataFrame(columns=RecordDef.schema.keys())
            df.to_pickle(db_path)
        else:
            raise OSError("collection db already exists!")
        return cls(collection_name, folder=folder)

    @classmethod
    def drop(cls, collection_name, folder=COLLECTIONS_FOLDER):
        """Delete df associated with a collection and remove folder if empty."""
        db_path = cls.return_db_path(collection_name, folder=folder)
        if os.path.exists(db_path):
            os.remove(db_path)
        if len(os.listdir(folder)) == 0:
            os.remove(folder)

    @staticmethod
    def return_db_path(collection_name, folder=COLLECTIONS_FOLDER):
        """Return path for collection records df."""
        records_path = os.path.join(folder, collection_name, "records.pkl")
        records_path = records_path.replace(" ", "_")
        return records_path

    def update_record(self, record):
        """Add or update a record in the df."""
        record_id = record["record_id"]
        self.df.loc[record_id] = record

    def return_record(self, record_id):
        """Return record associated with record_id."""
        record = self.df.loc[record_id].to_dict()
        return record

    def rm_record(self, record_id):
        """Remove a record from the df."""
        try:
            self.df.drop(record_id, inplace=True)
        except KeyError:
            print("warning: no record to remove at {}".format(record_id))

    def write_db(self):
        """Write/save current state of the database to file."""
        self.df.to_pickle(self.db_path)


class Collection(object):
    """A facade class for interfacing with document collections.

    Includes high level api for collection management and error handling. Also
    handles collection-level methods e.g. tf/idf keyword generation.
    """

    client = search.Client()
    search.Server().start()
    ssh_client = ssh_utils.SSHClient()
    collections_folder = COLLECTIONS_FOLDER
    db_path = os.path.join(collections_folder, "db_meta.pkl")

    def __init__(self, collection_name):
        self.name = collection_name
        self.data = Data(self.name, folder=Collection.collections_folder)
        self.df = self.data.df
        self.record_type = self.db_meta().loc[collection_name].record_type
        self.RecordDef = self.return_record_def(self.record_type)

    @property
    def summary(self):
        summary = {
            "name": self.name,
            "record type": self.record_type,
            "records": self.df.shape[0],
        }
        return summary

    @classmethod
    def db_meta(cls):
        """Generate db_meta from db_path."""

        db_meta_folder = os.path.dirname(cls.collections_folder)
        try:
            db_meta = pd.read_pickle(cls.db_path)
        except FileNotFoundError:
            print(f"no db found at {cls.db_path}, creating empty db_meta.")
            cls.create_db_meta()
            db_meta = pd.read_pickle(cls.db_path)
        return db_meta

    @classmethod
    def create_db_meta(cls):
        """Create a new db_meta at specified path if it doesn't exist."""
        if os.path.exists(cls.db_path):
            raise FileExistsError
        else:
            db_meta_folder = os.path.dirname(cls.db_path)
            if not os.path.exists(db_meta_folder):
                os.makedirs(db_meta_folder)
            db_meta = pd.DataFrame(columns=META_DB_COLS)
            db_meta.index.name = "collection"
            db_meta.to_pickle(cls.db_path)

    @classmethod
    def drop_db_meta(cls):
        """Remove db_meta at specified path if it exists."""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        else:
            print(f"no db_meta found at {cls.db_path}")

    @classmethod
    def new(
        cls, collection_name, RecordDef, folder=COLLECTIONS_FOLDER,
    ):
        """Create a new collection. """
        if collection_name in cls.db_meta().index:
            raise ValueError(f"collection with name {collection_name} already exists")

        meta_db_record = {
            "record_type": RecordDef.record_type,
            "creation_date": datetime.datetime.utcnow(),
        }
        if set(meta_db_record.keys()) != set(META_DB_COLS):
            raise ValueError("invalid schema for new meta_db record")

        # add row to df_collections
        db_meta = cls.db_meta().append(pd.Series(meta_db_record, name=collection_name))
        db_meta.to_pickle(cls.db_path)

        # now reasonbly certain collection objects don't exist: create Data, search index
        Data.new(collection_name, RecordDef, folder=folder)
        cls.client.new_index(
            collection_name=collection_name, mapping=RecordDef.index_mapping
        )
        return cls(collection_name=collection_name)

    @classmethod
    def drop(cls, collection_name, folder=COLLECTIONS_FOLDER):
        """Remove a collection.

        Try/except to avoid erring if index exists but db doesn't, etc.
        """
        try:
            Data.drop(collection_name, folder=folder)
        except Exception:
            print("unable to locate collection db.")
        try:
            df = cls.db_meta().drop(collection_name)
            df.to_pickle(cls.db_path)
        except Exception:
            print("unable to update db_meta.")
        try:
            cls.client.drop_index(collection_name)
        except HTTPError:
            print("error dropping collection from search index.")

    @staticmethod
    def return_record_def(record_type):
        """Return record_def from record type."""

        for record_def in RecordDef.__subclasses__():
            if record_def.record_type == record_type:
                return record_def
        raise Exception(
            (
                f"No record found for type {record_type} "
                "(import of associated RecordDef in collection.py directly)."
            )
        )

    def add_document(self, record_id):
        """Add a record to the collection."""
        record = self.RecordDef.gen_record(record_id)
        self.add_record(record)

    def _add_record(self, record):
        """Generate record from record_id; add to collection but don't save."""
        (record_id, record_index) = self.RecordDef.gen_record_index(record)
        self.data.update_record(record)
        type(self).client.index_record(
            record_id=record_id, record_index=record_index, collection_name=self.name
        )

    def add_record(self, record):
        """Add a given record to the collection, save the database."""
        self._add_record(record)
        self.data.write_db()

    def query_source(self, *args, **kwargs):
        """Generate record(s) from an external source.

        A source, query_str, and **kwargs together imply a collection of records, a convenience
        tool when many records are desired to get at once.  It remains generic so as not to
        put constraints on how this may be implemented by record_def.

        Examples:
        "/Users/username/Documents", {"file_extensions":[".txt"]} -> All text files in Documents
        "some_query_string" {"params": [1, 20, 4]} -> all records associated with a web query
        """
        records_list = self.RecordDef.query_source(*args, **kwargs)
        return records_list

    def remove_record(self, record_id):
        """Remove record from collection; inverse of add_document."""
        self.data.rm_record(record_id)
        self.data.write_db()
        self.client.delete_record(record_id, collection_name=self.name)

    def remove_records(self, record_id):
        """Remove records from collection; inverse of add_documents"""
        self.data.rm_record(record_id)
        self.data.write_db()
        self.client.delete_record(record_id, collection_name=self.name)

    def return_record(self, record_id):
        """return record dict from record_id"""
        ser = self.df.loc[record_id]
        record = ser.to_dict()
        return record

    def _raw_query(self, query_str):
        """Return raw query result json."""
        query_results = self.client.query(
            collection_name=self.name, query_str=query_str
        )
        return query_results

    def query_records(self, query_str):
        """return record ids from query_str."""
        res = self._raw_query(query_str)
        results = res["hits"]["hits"]
        record_score_dict = {r["_id"]: r["_score"] for r in results}
        return record_score_dict

    def open_document(self, record_id):
        """Open record (edit ok now) with associated executable.

        Write db as record access_times have been updated.
        """
        self.RecordDef.open_doc(df=self.df, record_id=record_id)
        self.data.write_db()
