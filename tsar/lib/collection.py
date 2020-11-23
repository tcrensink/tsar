"""This module contains:
- DataBase class:   handles storage addition/removal of records
- Collection class: high level interface for attribute objects DataBase, Client, Browser, RecordDef, etc.

- Lookup functions to find associated RecordDef
"""
import logging
import os
import json
import pandas as pd
from pickle import UnpicklingError
from requests.exceptions import HTTPError
from tsar.doctypes import DOCTYPES
from tsar.doctypes.doctype import update_dict, DocTypeResolver
from tsar.doctypes.arxiv_doc import ArxivDoc
from tsar.doctypes.markdown_doc import MarkdownDoc
from tsar import COLLECTIONS_FOLDER, HOST_REPO_PATH, LOG_FOLDER
from tsar.config import DEFAULT_COLLECTION
from tsar.lib.record_defs.parse_lib import resolve_path
from tsar.lib import search
from tsar.lib.search import return_index_name
from tsar.lib.record_def import RecordDef
import datetime
from requests import HTTPError

REGISTER_PATH = os.path.join(COLLECTIONS_FOLDER, "collection_register.pkl")

logger = logging.getLogger(__name__)
handler = logging.FileHandler(os.path.join(LOG_FOLDER, "collection.log"))
logger.addHandler(handler)


class Data(object):
    """Database for parsed document records."""

    def __init__(self, df, index_field="document_id"):
        if df.index.name != index_field:
            raise ValueError(f"index field required to be `{index_field}`")
        self.df = df

    def __repr__(self):
        value = "data:\n" + self.df.__repr__()
        return value

    @classmethod
    def new(cls, record_schema, index_field="document_id"):
        if index_field not in record_schema.keys():
            raise KeyError(
                f"did not find expected index field `{index_field}` in schema."
            )
        df = pd.DataFrame(columns=record_schema.keys())
        df = df.set_index(index_field, drop=True)
        return cls(df)

    @classmethod
    def read(cls, path):
        df = pd.read_pickle(path)
        return cls(df=df)

    def write(self, path, force=True):
        """Write/save current state of the database to file."""
        path = resolve_path(path)
        path_exists = os.path.exists(path)
        if path_exists and not force:
            raise OSError("file already exists!")
        elif path_exists and force:
            self.df.to_pickle(path)
        elif not path_exists:
            db_folder = os.path.dirname(path)
            os.makedirs(db_folder, exist_ok=True)
            self.df.to_pickle(path)

    @classmethod
    def drop(cls, path):
        """Remove db file."""
        if os.path.exists(path):
            try:
                # verify filetype before deleting
                _ = cls.read(path)
                os.remove(path)
            except UnpicklingError("Aborted: not a database file."):
                return
            except FileNotFoundError:
                logger.exception(f"nothing to delete at {path}")

    def update_record(self, record):
        """Add or update a record in the df."""
        document_id = record["document_id"]
        self.df.loc[document_id] = record

    def return_record(self, document_id):
        """Return record associated with doc_id."""
        if document_id in self.df.index:
            record = self.df.loc[document_id].to_dict()
        else:
            record = None
        return record

    def rm_record(self, document_id):
        """Remove the record associated with doc_id."""
        try:
            self.df.drop(document_id, inplace=True)
        except KeyError:
            logger.exception("warning: no record to remove at {}".format(document_id))


class Register(object):
    """Collection registry to manage stateful collection assets.

    Read/write from disk every time to ensure state is consistent; invoked through Collection.register
    """

    def __init__(self, path=REGISTER_PATH, schema=None):

        if schema is None:
            schema = {
                "records_db_path": object,
                "config_path": object,
                "search_indices": object,
            }
        self.schema = schema
        self.path = path
        if not os.path.exists(path):
            df = pd.DataFrame(columns=self.schema.keys())
            df.index.name = "collection_id"
            df.to_pickle(path)

    def read_df(self):
        df = pd.read_pickle(self.path)
        return df

    def _write(self, df):
        df.to_pickle(self.path)

    def exists(self, collection_id):
        df = pd.read_pickle(self.path)
        return True if collection_id in df.index else False

    def add(self, collection_record):
        """Register a collection."""
        collection_id = collection_record.pop("collection_id")

        df = self.read_df()
        if collection_id in df.index:
            raise KeyError(f"collection {collection_id} already registered.")

        missing_fields = set(self.schema.keys()) - set(collection_record.keys())
        if missing_fields:
            raise ValueError(f"collection_kwargs missing {missing_fields}")

        df.loc[collection_id] = collection_record
        self._write(df)

    def drop(self, collection_id):
        """Unregister a collection."""
        df = self.read_df()
        if collection_id in df.index:
            df = df.drop(collection_id)
        else:
            logger.warn(f"collection {collection_id}; not found in registry to remove.")
        self._write(df)

    def return_record(self, collection_id):
        """Return collection asset paths."""
        df = self.read_df()
        return df.loc[collection_id].to_dict()


class Collection(object):
    """A high-level class for interfacing with document collections.

    Collections are considered temporary/in-memory until registered.
    Attributes `registered` and `_collection_id` are used to mark indexes as temporary.  The register is intended to
    be global.
    """

    search.Server().start()
    client = search.Client()
    _register = Register()

    def __init__(
        self, collection_id, doc_types, records_db, configd,
    ):
        """Initialize a Collection.

        Note:
        - init defines member variables/attributes for a collection object; other constructors define such objects
        as convenient and return cls.__init__().

        - config created or verified as consistent with provided fields
        """
        self.doctype_resolver = DocTypeResolver(doc_types)
        self.collection_id = collection_id
        self.doc_types = doc_types
        self.records_db = records_db
        self.configd = configd
        self.registered = self._register.exists(collection_id)

    @property
    def _collection_id(self):
        if self.registered:
            return self.collection_id
        else:
            return f"tmp_{self.collection_id}"

    @classmethod
    def new(cls, collection_id, doc_types):
        """Create a new collection.

        Until registered, collection assets are in-memory/overwritable.
        """
        # create records db
        collection_schema = {}
        for doc_type in doc_types:
            collection_schema = update_dict(collection_schema, doc_type.schema)
        records_db = Data.new(collection_schema)

        # create/overwrite temporary search indexes
        _collection_id = f"tmp_{collection_id}"
        search_indices = []
        for doc_type in doc_types:
            index_name = return_index_name(_collection_id, doc_type.__name__)
            search_indices.append(index_name)
            # overwrite temp indices of same name if they exist
            if cls.client.index_exists(index_name):
                cls.client.drop_index(index_name)
            cls.client.new_index(index_name=index_name, mapping=doc_type.index_mapping)

        configd = {
            "doc_types": [doc_type.__name__ for doc_type in doc_types],
        }
        coll = cls(
            collection_id=collection_id,
            doc_types=doc_types,
            records_db=records_db,
            configd=configd,
        )
        coll.search_indices = search_indices
        return coll

    @classmethod
    def registered_collections(cls):
        colls = cls._register.read_df().index.to_list()
        return colls

    @classmethod
    def clear_tmp_collections(cls, index_str="tmp_*"):
        cls.client.drop_index(index_str)

    def register(self, records_db_path=None, config_path=None, write=True):
        """Register collection/define asset paths.

        Registration (and subsequent collection.write) are used to create a persistent collection
        from an "in-memory" collection.  Paths and search index references are stored in a record keyed
        by collection name.
        """
        if self._register.exists(self.collection_id):
            raise KeyError(f"collection name {self.collection_id} already taken.")

        if records_db_path is None:
            records_db_path = os.path.join(
                COLLECTIONS_FOLDER, self.collection_id, "records.pkl"
            )
        if config_path is None:
            config_path = os.path.join(
                COLLECTIONS_FOLDER, self.collection_id, "config.json"
            )

        # rename temp indexes to collection
        search_indices = []
        for doc_type in self.doc_types:
            tmp_index_name = return_index_name(self._collection_id, doc_type.__name__)
            index_name = return_index_name(self.collection_id, doc_type.__name__)
            self.client.rename_index(
                index_name=tmp_index_name, new_index_name=index_name
            )
            search_indices.append(index_name)

        # register record, add attributes to collection
        collection_record = {
            "collection_id": self.collection_id,
            "records_db_path": records_db_path,
            "config_path": config_path,
            "search_indices": search_indices,
        }
        self._register.add(collection_record)
        for k, v in collection_record.items():
            setattr(self, k, v)
        self.registered = True
        if write:
            self.write()

    def _write_records_db(self, path, force=True):
        """Write records_db to file."""
        self.records_db.write(path, force=force)

    def _write_config(self, path, force=True):
        """Write config to file."""
        with open(path, "w") as fp:
            json.dump(self.configd, fp)

    def write(self, force=True):
        """Save state of collection defined in register record."""
        if not self.registered:
            raise KeyError(f"Collection must be registered before writing to file.")
        record = self._register.return_record(self.collection_id)
        records_db_path = record["records_db_path"]
        config_path = record["config_path"]

        # write assets
        self._write_records_db(records_db_path, force=force)
        self._write_config(config_path, force=force)

    @classmethod
    def load(cls, collection_id):
        """Load collection from assets saved to folder."""
        try:
            coll_record = cls._register.return_record(collection_id=collection_id)
        except KeyError:
            logger.exception("collection not found in register.")

        records_db = Data.read(coll_record["records_db_path"])
        with open(coll_record["config_path"], "r") as fp:
            configd = json.load(fp)
        doc_types = [DOCTYPES[doc_name] for doc_name in configd["doc_types"]]
        coll = cls(
            collection_id=collection_id,
            doc_types=doc_types,
            configd=configd,
            records_db=records_db,
        )
        # add register values as attributes
        for k, v in coll_record.items():
            setattr(coll, k, v)
        return coll

    @classmethod
    def drop(cls, collection_id):
        """Remove all assets associated with collection_id referenced in register."""

        # find record in register
        try:
            coll_record = cls._register.return_record(collection_id)
            cls._register.drop(collection_id)
        except KeyError:
            logger.exception(f"Unable to find record for {collection_id} in register.")
            return

        # get asset paths
        try:
            records_db_path = coll_record["records_db_path"]
            config_path = coll_record["config_path"]
            search_indices = coll_record["search_indices"]
        except KeyError:
            logger.exception(f"Unable to find asset paths in register.")

        # remove records_db
        try:
            os.remove(coll_record["records_db_path"])
        except FileNotFoundError:
            logger.exception(f"Unable to find {records_db_path} for removal.")

        # remove config path
        try:
            os.remove(config_path)
        except FileNotFoundError:
            logger.exception(f"Unable to find {config_path} for removal.")

        # remove collection indices
        for index_id in search_indices:
            try:
                cls.client.drop_index(index_name=index_id)
            except Exception:
                logger.exception(f"warning: unable to remove {index_id}")

    def _resolve_link_id(self, link_id, doc_type=None):
        """Resolve document_id using doctype_resolver for link ids."""
        if doc_type is None:
            try:
                doc_type = self.doctype_resolver.return_doctype(link_id)
            except Exception:
                logger.exception(f"unable to determine doctype of {link_id}")
        try:
            link_id = doc_type.resolve_id(link_id)
        except Exception:
            logger.exception(
                f"tried to resolve link_id: {link_id} using doctype: {doc_type}"
            )
        return link_id

    def gen_link_content(self, document_id):
        """Append content from linked docs."""
        df = self.records_db.df
        links = df.loc[document_id].links
        # link content series for link records in df:
        content_series = df[df.index.isin(links)].content
        link_content = "\n".join(content_series)
        return link_content

    def primary_documents(self):
        """Return index of primary document_ids."""
        df = self.records_db.df
        return df[df.primary_doc].index

    def add_document(
        self,
        document_id,
        primary_doc=True,
        doc_type=None,
        gen_link_records=True,
        index_linked_content=True,
        write=True,
    ):
        """Create a record, add it to the collection.

        - resolve link ids
        - optionally, generate records for links, add
            linked content to primary doc search index.
        """
        if doc_type is None:
            try:
                doc_type = self.doctype_resolver.return_doctype(document_id)
            except Exception:
                logger.exception(f"unable to determine doc_type for {document_id}")
                return
        record = doc_type.gen_record(
            document_id, primary_doc=primary_doc, gen_links=True
        )
        # resolve link_ids
        resolved_links = [self._resolve_link_id(link) for link in record["links"]]
        record["links"] = resolved_links

        # generate records for linked docs that aren't primary
        if gen_link_records:
            link_only_ids = [
                link for link in resolved_links if link not in self.primary_documents()
            ]
            for link_id in link_only_ids:
                self.add_document(
                    document_id=link_id,
                    primary_doc=False,
                    doc_type=None,
                    gen_link_records=False,
                    index_linked_content=False,
                )
            self.add_record(record, index_linked_content=False, write=False)
        self.add_record(record, index_linked_content=True, write=write)

    def add_record(self, record, index_linked_content, write=True):
        """Add record to collection, write to disk if registered."""
        self.records_db.update_record(record)
        if self.registered:
            self.records_db.write(self.records_db_path)
        doc_type = record["document_type"]
        if index_linked_content:
            link_content = self.gen_link_content(record["document_id"])
        else:
            link_content = None
        (document_id, record_index) = doc_type.gen_search_index(
            record, link_content=link_content
        )
        index_name = return_index_name(
            self._collection_id, doc_type_str=doc_type.__name__
        )
        self.client.index_record(
            document_id=document_id, record_index=record_index, index_name=index_name
        )

    def remove_record(self, document_id):
        """Remove (resolved) document_id record from collection."""

        # get doc_type to remove from search index
        record = self.records_db.return_record(document_id)
        self.records_db.rm_record(document_id)
        if self.registered:
            self.records_db.write(self.records_db_path)
        doc_type = record["document_type"]
        index_name = return_index_name(
            self._collection_id, doc_type_str=doc_type.__name__
        )
        self.client.delete_record(document_id, index_name=index_name)

    def return_record(self, document_id):
        return self.records_db.return_record(document_id)

    def _raw_query(self, query_str):
        """Return raw query result json."""
        query_results = self.client.query(
            index_list=self.search_indices, query_str=query_str
        )
        return query_results

    def query_records(self, query_str, primary_docs_only=True):
        """return record ids from query_str."""
        res = self._raw_query(query_str)
        results = res["hits"]["hits"]
        record_score_dict = {r["_id"]: r["_score"] for r in results}
        if primary_docs_only:
            primary_ids = set(self.primary_documents())
            record_score_dict = {
                k: v for k, v in record_score_dict.items() if k in primary_ids
            }
        return record_score_dict

    def add_from_source(self, doc_type, source_id, *source_args, **source_kwargs):
        """Add doc_type records from source_id."""
        doc_type = DOCTYPES[doc_type]
        document_ids = doc_type.gen_from_source(
            source_id, *source_args, **source_kwargs
        )
        for document_id in document_ids:
            self.add_document(document_id=document_id, doc_type=doc_type, write=False)
        if self.registered:
            self.write()
