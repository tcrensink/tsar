"""
General-purpose record for text files that (optionally) follows links and integrates in record
"""
import os
from datetime import datetime
from tsar import config
from tsar.lib.record_def import RecordDef, BASE_SCHEMA, SafeSerializer
from tsar.lib.record_defs import parse_lib, parsers
from tsar.lib.record_defs.wiki_record import WikiRecord
from tsar.lib.record_defs.arxiv_def import ArxivRecord
from pygments.lexers.markup import MarkdownLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name

SERIALIZER = SafeSerializer()

RECORD_TYPE = "omni"

# schema for omni record
SCHEMA = {
    "content": str,
    "links": dict,
    "access_times": list,
    "keywords": list,
}

# ES mapping.  linked_docs contains an id ('keyword' type) and content (text type) 
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "path": {"type": "text",},
            "content": {"type": "text", "analyzer": "english"},
            "links": {
                "properties": {
                    "source_id": {"type": "keyword"},
                    "source_content": {"type": "text"},
                },
            },
            "access_times": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_second",
            },
            "keywords": {"type": "keyword"},
        }
    }
}

class OmniRecord(RecordDef):
    """Defines markdown-based text doc that captures and indexes links."""

    record_type = RECORD_TYPE
    base_schema = BASE_SCHEMA
    schema = SCHEMA
    schema.update(BASE_SCHEMA)
    index_mapping = INDEX_MAPPING
    preview_lexer = MarkdownLexer
    preview_style = style_from_pygments_cls(get_style_by_name("solarizeddark"))

    @staticmethod
    def gen_link_content(link_list, source_path):
        """Generate content from links from source_path and return as dict `link_content`.
        source_path included to resolve relative (file path) links.
        """
        link_content = {}

        for link_id in link_list:
            doc_type = parsers.infer_type(link_id)        
            if doc_type not in parsers.PARSABLE_DOC_TYPES:
                link_content[link_id] = ""
            elif doc_type in parsers.TEXTFILE_DOCTYPE_MAP.values():
                doc_dict = parsers.parse_textfile(link_id, source_path=source_path)
                link_id = doc_dict["record_id"]
                link_content[link_id] = doc_dict["content"]
            elif doc_type == "arxiv":
                arxiv_content = parsers.parse_arxiv_url(link_id)["summary"]
                link_content[link_id] = arxiv_content
            else:
                raise ValueError("unable to parse document.")

        return link_content

    @staticmethod
    def gen_record(record_id):
        """Parse doc into a record; return it."""
        # parsing functions associated with specific doc type:
        parsed_doc = parsers.parse_textfile(record_id)
        record_id = parsed_doc["record_id"]

        # base schema
        record = {
            "record_id": record_id,
            "record_type": RECORD_TYPE,
            "record_name": record_id,
            "record_summary": parsed_doc["content"],
            "utc_last_access": parsed_doc["st_atime"],
        }

        # RecordDef-specific schema
        record["content"] = parsed_doc["content"]
        record["access_times"] = [parsed_doc["st_atime"]]

        # generate link content
        links = parse_lib.return_links(parsed_doc["content"])
        record["links"] = OmniRecord.gen_link_content(links, source_path=record_id)        
        record["keywords"] = parse_lib.text_to_keyword_linked_doc(
            doc_text=record["content"], 
            link_texts=list(record["links"].values()), 
            N=8,
        )
        return record

    @classmethod
    def query_source(cls, source_ref):
        """Return records associated with a source (query url, folder, etc)."""
        raise NotImplementedError

    @staticmethod
    def gen_record_index(record):
        """Generate search index entry for record."""
        record_id = record["record_id"]
        record_index = {
            "path": record_id,
            "content": record["content"],
            "links": record["links"],
            "access_times": max(record["access_times"]),
            "keywords": record["keywords"],
        }
        return (record_id, record_index)

    @staticmethod
    def _open_doc(record_id):
        """Open doc from record_id."""
        parse_lib.open_textfile(cmd=config.OPEN_TEXT_CMD, file_path=record_id)

    @staticmethod
    def open_doc(df, record_id):
        """open document associated with record, update metadata."""
        curr_time = parse_lib.utc_now_timestamp()
        df.loc[record_id, "utc_last_access"] = curr_time
        df.loc[record_id, "access_times"].append(curr_time)
        WikiRecord._open_doc(record_id)

    @staticmethod
    def update_collection(record_list):
        """Modifications to records that depend on collection."""
        pass
