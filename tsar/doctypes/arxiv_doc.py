import arxiv
import pandas as pd
from datetime import datetime
import requests
from tsar.doctypes.doctype import DocType, update_dict, BASE_SCHEMA, BASE_MAPPING
from tsar.lib.record_defs import parse_lib


class ArxivDoc(DocType):
    """Arxiv publication document type."""

    schema = {
        "authors": object,
        "publish_date": float,
    }
    schema = update_dict(schema, BASE_SCHEMA)

    index_mapping = {
        "mappings": {
            "properties": {
                "publish_date": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_second",
                },
                "authors": {"type": "text", "analyzer": "standard"},
            }
        }
    }
    index_mapping = update_dict(index_mapping, BASE_MAPPING)

    @staticmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate record from arxiv url.
        # example document_id: https://arxiv.org/abs/1810.04805
        arxiv reference: https://arxiv.org/help/api/user-manual#_calling_the_api
        # api url = 'http://export.arxiv.org/api/query?id_list=1311.5600'
        """
        paper_id = document_id.split("abs/")[-1]
        record_dict = arxiv.query(id_list=[paper_id])[-1]
        record = gen_record_from_arxiv_dict(record_dict, primary_doc=primary_doc)
        return record

    @staticmethod
    def gen_search_index(record, link_content=None):
        """Generate a search index from a record."""
        document_id = record["document_id"]
        record_index = {
            "document_name": record["document_name"],
            "content": record["content"],
            "authors": record["authors"],
            "publish_date": record["publish_date"],
            "link_content": link_content,
        }
        return (document_id, record_index)

    @staticmethod
    def gen_links(text):
        """Return citations found in text."""
        return []

    @staticmethod
    def gen_from_source(source_id, *source_args, **source_kwargs):
        """Return document ids from a document source (e.g. folder or query)."""
        pass

    @staticmethod
    def resolve_id(document_id):
        arxiv_dict = ArxivDoc.gen_record(document_id, primary_doc=None, gen_links=False)
        return arxiv_dict["document_id"]

    @staticmethod
    def resolve_source_id(source_id):
        return source_id

    @staticmethod
    def is_valid(document_id):
        url = requests.urllib3.util.parse_url(document_id)
        cond1 = bool(url.host == "arxiv.org")
        cond2 = bool(url.path.startswith("/abs"))
        if cond1 and cond2:
            return True
        else:
            return False

    @staticmethod
    def preview(record):

        preview = (
            f"{record['document_name']}\n"
            f"{pd.to_datetime(record['publish_date'], unit='s').isoformat()}"
            f"{', '.join(record['authors'])}"
            f"Abstract: {record['content']}"
        )
        return preview

def gen_record_from_arxiv_dict(arxiv_dict, primary_doc):
    """Parse arxiv package result into a record."""
    abstract = arxiv_dict["summary"].replace("\n", " ")
    title = arxiv_dict["title"].replace("\n", "")
    publish_date = int(datetime(*arxiv_dict["published_parsed"][:6]).timestamp())
    links = ArxivDoc.gen_links(abstract)

    record = {
        "document_id": arxiv_dict["id"],
        "document_name": title,
        "document_type": ArxivDoc,
        "primary_doc": primary_doc,
        "content": abstract,
        "authors": arxiv_dict["authors"],
        "publish_date": publish_date,
        "links": links,
    }
    return record
