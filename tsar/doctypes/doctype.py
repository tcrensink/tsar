from abc import ABC, abstractmethod
import collections.abc

# required fields for all DocTypes; used by app/framework.  Uses pandas/numpy dtypes.
BASE_SCHEMA = {
    "document_id": object,
    "document_name": object,
    "document_type": type,
    "primary_doc": bool,
    "content": object,
    "links": object,
}

ELASTICSEARCH_TYPES = ("text", "keyword", "date", "long", "double", "boolean", "ip")
# search index map
BASE_MAPPING = {
    "mappings": {
        "properties": {
            "document_name": {"type": "text", "analyzer": "english"},
            "content": {"type": "text", "analyzer": "english"},
            "link_content": {"type": "text", "boost": 0.2, "analyzer": "english"},
        }
    }
}

# nested dict update
def update_dict(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d


class DocType(ABC):
    """Defines how a document is parsed, indexed."""

    # base record schema, search index_mapping
    @property
    @classmethod
    @abstractmethod
    def schema(cls):
        return BASE_SCHEMA

    @property
    @classmethod
    @abstractmethod
    def index_mapping(cls):
        return BASE_MAPPING

    @staticmethod
    @abstractmethod
    def gen_record(document_id, primary_doc, gen_links):
        """Generate a record {document_id, field_dict} from a document_id."""
        pass

    @staticmethod
    @abstractmethod
    def gen_search_index(record, link_content):
        """Generate a search index entry from a record."""
        pass

    @staticmethod
    @abstractmethod
    def gen_links(text):
        """Parse text for links using DocType-specifics syntax."""
        pass

    @staticmethod
    @abstractmethod
    def gen_from_source(source_id, *source_args, **source_kwargs):
        """Return document ids from a document source (e.g. folder or query)."""
        pass

    @staticmethod
    @abstractmethod
    def resolve_id(document_id):
        """Resolve id to be unique for each document."""
        pass

    @staticmethod
    @abstractmethod
    def resolve_source_id(source_id):
        """Resolve source id."""
        pass

    @staticmethod
    @abstractmethod
    def is_valid(document_id):
        """Returns True if document_id is valid for doc type; expected to be performant."""
        pass

    @staticmethod
    @abstractmethod
    def preview(record):
        """(Text) preview of a document."""
        pass


class DocTypeManager(object):
    """Define record generation and link management when multiple doc types are present."""
    def __init__(self, doctypes):
        self.doctypes = doctypes

    def return_doctype(self, document_id):
        """Return best doctype for document_id."""
        if not isinstance(document_id, str):
            raise Exception(f"document_id not a string")
        for doctype in self.doctypes.values():
            if doctype.is_valid(document_id):
                return doctype
        raise Exception("No associated doctype")

    def gen_record(self, document_id, primary_doc, gen_links):
        """Source the correct doctype, generate a record for document_id."""
        doctype = self.return_doctype(document_id)
        record = doctype.gen_record(document_id, primary_doc, gen_links)

        # discard links with no valid doctype
        if gen_links:
            valid_links = set()
            for link_id in record["links"]:
                try:
                    doc_type = self.return_doctype(link_id)
                    resolved_link = self.resolve_document_id(link_id, doc_type=doc_type)
                    valid_links.add(resolved_link)
                except Exception:
                    # no associated doctype; discard link
                    pass
            record["links"] = list(valid_links)
        return record

    def resolve_document_id(self, link_id, doc_type=None):
        """Resolve document_id using doctype_resolver for link ids."""
        if doc_type is None:
            doctype = self.return_doctype(document_id)
        resolved_doc_id = doc_type.resolve_id(link_id)
        return resolved_doc_id
