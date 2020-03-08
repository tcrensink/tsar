"""
Define wiki record creation from a .md wiki file.
"""
# import os
from datetime import datetime
from tsar import config
from tsar.lib.record_def import RecordDef, BASE_SCHEMA, SafeSerializer
from tsar.lib.record_defs import parse_lib
from pygments.lexers.markup import MarkdownLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

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

VALID_EXTENSIONS = (
    ".md",
)


class WikiRecord(RecordDef):
    """Defines wiki doc -> wiki_record and downstream processing."""

    record_type = RECORD_TYPE
    base_schema = BASE_SCHEMA
    schema = SCHEMA
    schema.update(BASE_SCHEMA)
    index_mapping = INDEX_MAPPING
    preview_lexer = MarkdownLexer
    preview_style = style_from_pygments_cls(get_style_by_name('solarizeddark'))

    @staticmethod
    def gen_record(path):
        """Parse doc into a record; return it."""

        record_id = parse_lib.resolve_path(path)
        record_id = str(record_id)

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
        try:
            record["keywords"] = list(parse_lib.basic_text_to_keyword(raw_doc, 6))
        except Exception:
            return None
        return record

    @staticmethod
    def gen_records(folder):
        """Return records for docs of valid extension within a folder."""
        paths = parse_lib.return_files(folder, extensions=VALID_EXTENSIONS)
        records = []
        for path in paths:
            record = WikiRecord.gen_record(path)
            if record:
                records.append(record)
        return records

    @staticmethod
    def gen_record_index(record):
        """Generate search index entry for record."""
        record_id = record["record_id"]
        record_index = {}
        record_index["content"] = record["content"]
        record_index["access_times"] = max(record["access_times"])
        record_index["keywords"] = record["keywords"]
        return (record_id, record_index)

    @staticmethod
    def _open_doc(record_id):
        """Open doc from record_id."""
        parse_lib.open_textfile(path=record_id, editor=config.EDITOR)

    @staticmethod
    def open_doc(df, record_id):
        """open document associated with record, update metadata."""
        curr_time = parse_lib.utc_now_timestamp()
        df.loc[record_id, "utc_last_access"] = curr_time
        df.loc[record_id, "access_times"].append(curr_time)
        WikiRecord._open_doc(record_id)


def return_record_name(doc):
    """Create display name for doc/content.

    To do: add logic.
    """
    return doc


def return_record_summary(raw_doc):
    """Create display summary of the raw_doc.

    To do: add logic.
    """
    return raw_doc
