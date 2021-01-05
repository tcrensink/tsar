from tsar.doctypes.arxiv_doc import ArxivDoc
from tsar.doctypes.doctype import DocType
from tests.resources.parsed_docs import PARSED_ARXIV_DOC

ARIXV_DOC_ID = "https://arxiv.org/abs/1311.5600"


def test_subclass():

    assert issubclass(ArxivDoc, DocType)
    assert isinstance(ArxivDoc(), DocType)


def test_gen_record():
    """Verify record generation matches expected output."""
    record = ArxivDoc.gen_record(ARIXV_DOC_ID, primary_doc=True, gen_links=True)
    assert PARSED_ARXIV_DOC == record
