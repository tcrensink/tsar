from bs4 import BeautifulSoup
import markdown
import os

from tsar.doctypes.doctype import DocType, update_dict, BASE_SCHEMA, BASE_MAPPING
from tsar.lib.record_defs import parse_lib


class MarkdownDoc(DocType):
    """Markdown document type."""

    schema = BASE_SCHEMA
    index_mapping = {
        "mappings": {
            "properties": {"document_name": {"type": "text", "analyzer": "english"},}
        }
    }
    index_mapping = update_dict(index_mapping, BASE_MAPPING)

    @staticmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate a record from a markdown file."""
        document_id = MarkdownDoc.resolve_id(document_id)
        raw_doc = parse_lib.return_file_contents(document_id)
        links = MarkdownDoc.gen_links(raw_doc) if gen_links else []
        links = [
            parse_lib.resolve_path(link, document_id) if os.path.exists(link) else link
            for link in links
        ]
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
            "content": record["content"],
            "link_content": link_content,
        }
        return (document_id, record_index)

    @staticmethod
    def gen_links(text):
        """Return links from markdown text."""
        html = markdown.markdown(text)
        soup = BeautifulSoup(html, features="html.parser")
        links = [link.get("href") for link in soup.findAll("a")]
        return links

    @staticmethod
    def gen_from_source(source_id, extensions=[".md"]):
        """Return markdown docs in folder."""
        doc_ids = parse_lib.return_files(source_id, extensions=extensions)
        doc_ids = [MarkdownDoc.resolve_id(doc_id) for doc_id in doc_ids]
        return doc_ids

    @staticmethod
    def resolve_id(document_id):
        return parse_lib.resolve_path(document_id)

    @staticmethod
    def is_valid(document_id, extensions=[".md"]):
        valid = (
            os.path.exists(document_id)
            and os.path.splitext(document_id)[-1] in extensions
        )
        return valid
