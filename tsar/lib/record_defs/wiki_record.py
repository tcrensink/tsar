"""
Define wiki record creation from a .md wiki file.
"""
# import os
import datetime
from tsar import config
from tsar.lib.record_def import RecordDef, BASE_SCHEMA, SafeSerializer
from tsar.lib.record_defs import parse_lib
SERIALIZER = SafeSerializer()

RECORD_TYPE = "wiki"

SCHEMA = {
    "content": str,
    "access_times": list,
    "keywords": set,
}

# elasticsearch mapping for content in each column
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "content": {
                "type": "text",
                "analyzer": "english"
            },
            "access_times": {
                "type": "date",
                "format": "epoch_second",
            },
            "keywords": {
                "type": "keyword"
            }
        }
    }
}

DOC_VIEWER = config.EDITOR
DOC_EDITOR = config.EDITOR


class WikiRecord(RecordDef):
    """Defines wiki doc -> wiki_record and downstream processing."""

    record_type = RECORD_TYPE
    base_schema = BASE_SCHEMA
    schema = SCHEMA
    schema.update(BASE_SCHEMA)
    index_mapping = INDEX_MAPPING

    @staticmethod
    def gen_record(record_id):
        """Parse doc into a record; return it."""

        raw_doc = parse_lib.return_raw_doc(record_id)
        file_info = parse_lib.file_meta_data(record_id)

        record = {}

        # BASE_SCHEMA fields
        record["record_id"] = record_id
        record["record_type"] = RECORD_TYPE
        record["record_name"] = return_record_name(record_id)
        record["record_summary"] = return_record_summary(raw_doc)
        record["utc_last_access"] = file_info["st_atime"]

        # SCHEMA fields
        record["content"] = raw_doc
        record["access_times"] = [file_info["st_atime"]]
        record["keywords"] = list(parse_lib.basic_text_to_keyword(raw_doc, 8))
        return record

    @staticmethod
    def gen_record_index(record):
        """Generate search index entry for record."""

        record_id = record["record_id"]
        record_index = {}
        record_index["content"] = record["content"]
        record_index["access_times"] = max(record["access_times"])
        record_index["keywords"] = record["keywords"]
        # record_index = SERIALIZER.dump(record_index)
        return (record_id, record_index)

    @staticmethod
    def view_doc(record):
        """open document associated with record to view"""
        parse_lib.open_textfile(path=record["record_id"], editor=DOC_VIEWER)
        record["access_times"].append(datetime.utcnow().timestamp())

    @staticmethod
    def edit_doc(record):
        """open doc associated with record to edit"""
        parse_lib.open_textfile(path=record["record_id"], editor=DOC_EDITOR)
        record["access_times"].append(datetime.utcnow().timestamp())


def return_record_name(doc):
    """Create name from doc/content.

    To do: add logic.
    """
    return doc


def return_record_summary(raw_doc):
    """Create summary of the raw_doc.

    To do: add logic.
    """
    return raw_doc
