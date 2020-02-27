"""
This module include the ABC required to create a new RecordType:
- BASE_SCHEMA,
- constants/defaults/templates for defining record behavior
- RecordDef ABC (later)

Elasticsearch mapping: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html
Elasticsearch analysers: https://www.elastic.co/guide/en/elasticsearch/reference/current/analyzer.html

- index types: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

List of validations when creating ABC:
- record types are uniquely named (automatic)
- parse is defined
- schema fields are all defined
- base/record schema and index mapping are consistent
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
    # "collection": str,
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
