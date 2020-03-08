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
"""
from tsar import config
from abc import ABC, abstractmethod
import datetime
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
    """The abstract base class that defines the interface for a record.

    Some abstractmethods are optional, and may be implemented with `pass`.  Examples:
    - `create_doc_from_selection` -> difficult to implement for doc type .png

    """
    # @abstractmethod
    # def __init__(self):
    #     pass

    @staticmethod
    @abstractmethod
    def gen_record(self, file):
        pass

    @staticmethod
    @abstractmethod
    def gen_record_index(self, file):
        pass
    # some feature ideas below:
    # @abstractmethod
    # def save_local_doc(self, record_id):
    #     """For Arxiv, this would save the pdf locally."""

    # @abstractmethod
    # def

    # def _validate_parser(self, parse_func, **kwargs):
    #     """verify parser generates record according to schema"""

    # def _validate_search_mapping(self):
    #     """verify search mapping inputs match schema fields, etc."""
