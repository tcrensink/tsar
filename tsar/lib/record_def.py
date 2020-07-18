"""
This module include the ABC required to create a new RecordType.

A RecordType subclass must implement the following:

- record_type: name of recorddef
- base_schema: record BASE_SCHEMA fields
- schema: additional type-specific record fields
- index mapping: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
- open_doc is implemented
- collection_update: update records/search indexes based on entire collection
- preview lexer (optional)
- preview style (optional)
- update_collection (can be no-op, but must be defined)

Validations to require with ABC:
- record_id is string (used to open doc with open_doc)
- record types are unique
- gen_record() implements all record fields
- no additional fields are generated
- base/record schema and index mapping are consistent (type check)
- verify INDEX_MAPPING["mappings"]["content"][:]["type"] are in set ELASTICSEARCH_TYPES
- handling of empty files/record values
"""

from tsar import config
from abc import ABC, abstractmethod
import datetime
import numpy as np
from elasticsearch.serializer import JSONSerializer

ELASTICSEARCH_TYPES = ("text", "keyword", "date", "long", "double", "boolean", "ip")

"""Fields required for all records, used by TSAR internals
- record_id: access to original doc; file path or uri
- record_type: associated with a record_def
- record_name: ~one line record display string
- record_summary: ~one paragraph summary/description, appears as document preview
- collection: unique collection name.  Multiple collections may share a single record_type.
- utc_last_access: used for temporal sorting
"""
BASE_SCHEMA = {
    "record_id": str,
    "record_type": str,
    "record_name": str,
    "record_summary": str,
    "utc_last_access": datetime.datetime,
}

DOC_VIEWERS = {
    ".txt": config.EDITOR,
    ".md": config.EDITOR,
}

DOC_EDITORS = {
    ".txt": config.EDITOR,
    ".md": config.EDITOR,
}


class SafeSerializer(JSONSerializer):
    """modify json serialization to handle sets"""

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, np.int64):
            return int(obj)
        return JSONSerializer.default(self, obj)


class RecordDef(ABC):
    """The abstract base class that defines the interface for a record."""

    @classmethod
    @abstractmethod
    def query_source(query_str):
        """Return records from source based on query_str.

        Examples:
        query_str="~/my_markdown_docs"
            return records associated with files in folder as parsed by RecordDef

        query_str="http://export.arxiv.org/api/query?search_query=all:electron+AND+all:proton"
            returns records for all docs associated with query_str
        """
        pass

    @staticmethod
    @abstractmethod
    def gen_record(doc_id):
        """Generate record for doc associated with doc_reference.

        doc_id specifies a document, but may not be a unique label.  For example, if ../my_file and
        ~/my_file point to the same file, they are valid doc_ids (whereas record_id is expected to be a unique
        reference, e.g. /users/username/my_file.)
        """
        pass

    @staticmethod
    @abstractmethod
    def gen_record_index(record):
        """Generate a search index record in elasticsearch for the record."""
        pass

    @staticmethod
    @abstractmethod
    def open_doc(record_id):
        """Open a document associated with record_id."""
        pass
