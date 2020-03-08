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
import atoma
import requests

SERIALIZER = SafeSerializer()

RECORD_TYPE = "arxiv"

SCHEMA = {
    # "content": str,
    "access_times": list,
    "keywords": set,
    "authors": list,
    "publish_date": float
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
            },
            "publish_date": {
                "type": "date",
                "format": "epoch_second",
            },
            "authors": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }
}


def recent_ml_and_ai_query_url(
    fields=["cs.AI", "cs.LG", "cs.CL", "cs.NE"],
    sort_method="lastUpdatedDate",
    max_results=4000,
):
    """Return query string for recent ml/ai papers."""
    base_query = "http://export.arxiv.org/api/query?search_query="
    fields_str = "+OR+".join([f"cat:{f}" for f in fields])
    sort_str = f"sortBy={sort_method}"
    max_results_str = f"max_results={max_results}"
    query = base_query + "&".join([fields_str, sort_str, max_results_str])
    return query


def gen_record_from_atom(content):
    """Parse arxiv result in atom XML format.

    e.g.:
    res = requests.get(arxiv_query_url)
    content = atoma.parse_atom_bytes(res.content).entries[0].
    """
    abstract = content.summary.value
    curr_time = parse_lib.utc_now_timestamp()

    record = {}
    # BASE_SCHEMA fields
    record["record_id"] = content.id_
    record["record_type"] = RECORD_TYPE
    record["record_name"] = content.title.value.replace("\n", "")
    record["record_summary"] = content.summary.value.replace("\n", "")
    record["utc_last_access"] = curr_time

    # SCHEMA fields
    record["access_times"] = [curr_time]
    record["keywords"] = list(parse_lib.basic_text_to_keyword(abstract, 6))
    record["authors"] = [author.name for author in content.authors]
    record["publish_date"] = content.published
    return record


class ArxivRecord(RecordDef):
    """Defines wiki doc -> wiki_record and downstream processing."""

    record_type = RECORD_TYPE
    base_schema = BASE_SCHEMA
    schema = SCHEMA
    schema.update(BASE_SCHEMA)
    index_mapping = INDEX_MAPPING
    preview_lexer = MarkdownLexer
    preview_style = style_from_pygments_cls(get_style_by_name('solarizeddark'))

    @staticmethod
    def gen_record(document_id):
        """Parse doc_id (url) into record and return it.

        ref: https://arxiv.org/help/api/user-manual#_calling_the_api
        # url = 'http://export.arxiv.org/api/query?id_list=1311.5600'
        """
        res = requests.get(document_id)
        content = atoma.parse_atom_bytes(res.content).entries[0]
        record = gen_record_from_atom(content)
        return record

    @staticmethod
    def gen_records(query_url=None):
        """Return records associated with query params.
        ref: https://arxiv.org/help/api/user-manual#Appendices
        """
        if query_url is None:
            query_url = recent_ml_and_ai_query_url()

        res = requests.get(url=query_url)
        results = atoma.parse_atom_bytes(res.content).entries

        records = []
        for content in results:
            record = gen_record_from_atom(content)
            records.append(record)
        return records

    @staticmethod
    def gen_record_index(record):
        """Generate search index entry for record."""
        record_id = record["record_id"]
        record_index = {}
        record_index["content"] = record["record_summary"]
        record_index["access_times"] = max(record["access_times"])
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
