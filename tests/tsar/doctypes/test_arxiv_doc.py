from tsar.doctypes.arxiv_doc import ArxivDoc
from tsar.doctypes.doctype import DocType

def test_subclass():

    assert issubclass(ArxivDoc, DocType)
    assert isinstance(ArxivDoc(), DocType)
