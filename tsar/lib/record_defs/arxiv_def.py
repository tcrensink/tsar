"""
Define arxiv record creation from a api endpoint.

See https://github.com/karpathy/arxiv-sanity-preserver

This RecordDef is pretty rough.  Todo:
- are these a Collection or a Catelogue?
- consider parsing full text instead of abstract (see arxiv sanity preserver)
- remove redundant paper versions
- make generate_records url more flexible
- compare existing records before adding new.
"""
from datetime import datetime
from tsar import config
from tsar.lib.record_def import RecordDef, BASE_SCHEMA, SafeSerializer
from tsar.lib.record_defs import parse_lib
from pygments.lexers.markup import MarkdownLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
import arxiv
import requests

SERIALIZER = SafeSerializer()

RECORD_TYPE = "arxiv"

SCHEMA = {
    # "content": str,
    "access_times": list,
    "keywords": set,
    "authors": list,
    "publish_date": float,
}

# elasticsearch mapping for content in each column
INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "title": {"type": "text", "analyzer": "english"},
            "content": {"type": "text", "analyzer": "english"},
            "access_times": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_second",
            },
            "keywords": {"type": "keyword"},
            "publish_date": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_second",
            },
            "authors": {"type": "text", "analyzer": "standard"},
        }
    }
}


def recent_ml_and_ai_query_url(
    fields=["cs.AI", "cs.LG", "cs.CL", "cs.NE"],
    sort_method="lastUpdatedDate",
    max_results=4,
):
    """Return query string for recent ml/ai papers."""
    base_query = "http://export.arxiv.org/api/query?search_query="
    fields_str = "+OR+".join([f"cat:{f}" for f in fields])
    sort_str = f"sortBy={sort_method}"
    max_results_str = f"max_results={max_results}"
    query = base_query + "&".join([fields_str, sort_str, max_results_str])
    return query


def gen_record_from_arxiv(arxiv_dict):
    """Parse arxiv package result into a record."""
    abstract = arxiv_dict["summary"]
    title = arxiv_dict["title"].replace("\n", "")
    curr_time = parse_lib.utc_now_timestamp()

    keyword_text = "{} {}".format(title, abstract)
    keywords = list(parse_lib.basic_text_to_keyword(keyword_text, 6))
    publish_date = int(datetime(*arxiv_dict["published_parsed"][:6]).timestamp())

    record = {
        # BASE SCHEMA fields:
        "record_id": arxiv_dict["id"],
        "record_type": RECORD_TYPE,
        "record_name": title,
        "record_summary": abstract,
        "utc_last_access": curr_time,
        # SCHEMA fields
        "access_times": [],
        "keywords": keywords,
        "authors": arxiv_dict["authors"],
        "publish_date": publish_date,
    }
    return record


class ArxivRecord(RecordDef):
    """Defines wiki doc -> wiki_record and downstream processing."""

    record_type = RECORD_TYPE
    base_schema = BASE_SCHEMA
    schema = SCHEMA
    schema.update(BASE_SCHEMA)
    index_mapping = INDEX_MAPPING
    preview_lexer = MarkdownLexer
    preview_style = style_from_pygments_cls(get_style_by_name("solarizeddark"))

    @staticmethod
    def gen_record(document_id):
        """Parse doc_id (url) into record and return it.

        # example doc_id: https://arxiv.org/abs/1810.04805
        ref: https://arxiv.org/help/api/user-manual#_calling_the_api
        # api url = 'http://export.arxiv.org/api/query?id_list=1311.5600'
        """
        # see https://arxiv.org/help/arxiv_identifier
        paper_id = document_id.split("abs/")[-1]
        record_dict = arxiv.query(id_list=[paper_id])[-1]
        record = gen_record_from_arxiv(record_dict)
        return record

    @staticmethod
    def query_source(query_str="", max_results=20, **query_kwargs):
        """Return records associated with query params.
        ref: https://arxiv.org/help/api/user-manual#Appendices
        """
        results = arxiv.query(
            query=query_str, 
            max_results=max_results, 
            sort_by="relevance", 
            **query_kwargs,
        )
        records = [gen_record_from_arxiv(res) for res in results]
        return records

    @staticmethod
    def gen_record_index(record):
        """Generate search index entry for record."""
        record_id = record["record_id"]
        record_index = {}
        record_index["title"] = record["record_name"]
        record_index["content"] = record["record_summary"]
        record_index["access_times"] = record["access_times"]
        record_index["authors"] = record["authors"]
        record_index["publish_date"] = record["publish_date"]
        record_index["keywords"] = record["keywords"]
        return (record_id, record_index)

    @staticmethod
    def _open_doc(record_id):
        """Open doc from record_id."""
        parse_lib.open_url(url=record_id, browser=config.BROWSER)

    @staticmethod
    def open_doc(df, record_id):
        """open document associated with record, update metadata."""
        curr_time = parse_lib.utc_now_timestamp()
        df.loc[record_id, "utc_last_access"] = curr_time
        df.loc[record_id, "access_times"].append(curr_time)
        ArxivRecord._open_doc(record_id)

    @staticmethod
    def update_collection(record_list):
        """Modifications to records that depend on collection."""
        pass
