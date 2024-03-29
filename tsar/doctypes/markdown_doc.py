from bs4 import BeautifulSoup
import logging
import mistune
import os

# from tsar import LOG_FOLDER
from tsar import LOG_FOLDER
from tsar.doctypes.doctype import DocType, update_dict, BASE_SCHEMA, BASE_MAPPING
from tsar.lib import parse_lib
from logging import FileHandler

handler = FileHandler(os.path.join(LOG_FOLDER, "markdown_doc.log"), mode="w+")
logger = logging.getLogger(__name__)
logger.addHandler(handler)


class MarkdownDoc(DocType):
    """Markdown document type."""

    schema = BASE_SCHEMA
    index_mapping = {"mappings": {"properties": {"document_name": {"type": "text",},}}}
    index_mapping = update_dict(index_mapping, BASE_MAPPING)

    @staticmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate a record from a markdown file."""
        document_id = MarkdownDoc.resolve_id(document_id)
        raw_doc = parse_lib.return_file_contents(document_id)
        raw_links = MarkdownDoc.gen_links(raw_doc) if gen_links else []
        links = []
        for link in raw_links:
            try:
                res_link = parse_lib.resolve_path(link, document_id)
            except AttributeError:
                logger.exception(f"unable to resolve link: {link}")
            if os.path.exists(res_link):
                links.append(res_link)
            else:
                links.append(link)
        record = {
            "document_id": document_id,
            "document_name": document_id,
            "primary_doc": primary_doc,
            "document_type": MarkdownDoc,
            "content": raw_doc,
            "links": links,
        }
        return record

    @staticmethod
    def gen_search_index(record, link_content=None):
        """Generate a search index entry from a record."""
        document_id = record["document_id"]
        record_index = {
            "document_name": record["document_id"],
            "document_type": record["document_type"].__name__,
            "content": record["content"],
            "link_content": link_content,
        }
        return (document_id, record_index)

    @staticmethod
    def gen_links(text):
        """Return links from markdown text."""
        html = mistune.html(text)
        soup = BeautifulSoup(html, features="html.parser")
        links = list(set([link.get("href") for link in soup.findAll("a")]))
        return links

    @staticmethod
    def gen_from_source(source_id, extensions=[".md"]):
        """Return markdown docs from folder source_id, recursively."""
        doc_ids = parse_lib.return_files(source_id, extensions=extensions)
        doc_ids = [MarkdownDoc.resolve_id(doc_id) for doc_id in doc_ids]
        return doc_ids

    @staticmethod
    def resolve_id(document_id):
        return parse_lib.resolve_path(document_id)

    @staticmethod
    def resolve_source_id(source_id):
        return parse_lib.resolve_path(source_id)

    @staticmethod
    def is_valid(document_id, extensions=[".md"]):

        cond1 = parse_lib.exists_on_fs(parse_lib.host_path_to_url(document_id))
        cond2 = os.path.splitext(document_id)[-1] in extensions
        return bool(cond1 and cond2)

    @staticmethod
    def preview(record):

        preview_text = "(file contents):\n" f'{record["content"]}'
        return preview_text
