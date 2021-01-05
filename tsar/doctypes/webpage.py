"""Generic webpage.  Defer to custom webpage/url doctypes if they exist."""
from bs4 import BeautifulSoup
from datetime import datetime
import html2text
import requests
from tsar.doctypes.doctype import DocType, update_dict, BASE_SCHEMA, BASE_MAPPING
from tsar.lib import parse_lib


class WebpageDoc(DocType):
    """Generic url/html document type."""
    schema = BASE_SCHEMA
    index_mapping = BASE_MAPPING

    @staticmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate record from url.

        # example document_id: https://www.bookbub.com/blog/free-short-stories-online
        """
        h = html2text.HTML2Text()
        res = requests.get(document_id)
        text = h.handle(res.content.decode())

        # get title:
        soup = BeautifulSoup(markup=res.text, features="html.parser")
        try:
            title = soup.find("title").text
        except Exception:
            title = "(no title available)"
        links = []
        record = {
            "document_id": document_id,
            "document_name": title,
            "primary_doc": primary_doc,
            "document_type": WebpageDoc,
            "content": text,
            "links": links,
        }
        return record

    @staticmethod
    def gen_search_index(record, link_content=None):
        """Generate a search index from a record."""
        document_id = record["document_id"]
        record_index = {
            "document_name": record["document_name"],
            "content": record["content"],
        }
        return (document_id, record_index)

    @staticmethod
    def gen_links(text):
        """Return links found in text."""
        return []

    @staticmethod
    def gen_from_source(source_id, *source_args, **source_kwargs):
        """Return document ids from a document source (e.g. folder or query)."""
        pass

    @staticmethod
    def resolve_id(document_id):
        return document_id

    @staticmethod
    def resolve_source_id(source_id):
        return source_id

    @staticmethod
    def is_valid(document_id):
        url = requests.urllib3.util.parse_url(document_id)
        cond1 = bool(url.host != None)
        cond2 = bool(url.scheme != None)
        if cond1 and cond2:
            return True
        else:
            return False

    @staticmethod
    def preview(record):

        preview = (
            f"{record['document_name']}\n"
            f"Preview: {record['content'][0:1200]}"
        )
        return preview
