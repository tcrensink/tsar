import os
import pytest
from tsar.doctypes.webpage import WebpageDoc
from tsar.doctypes.doctype import DocType
from tsar import TESTS_FOLDER, TEST_FIXTURES_FOLDER, TEST_RESOURCES_FOLDER
from tests.resources.parsed_docs import PARSED_WEBPAGE_DOC

WEBPAGE_DOC_ID = "https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html"



def test_subclass():
    assert issubclass(WebpageDoc, DocType)
    assert isinstance(WebpageDoc(), DocType)

def test_gen_record():
    """Verify record generation matches expected output."""
    record = WebpageDoc.gen_record(WEBPAGE_DOC_ID, primary_doc=True, gen_links=True)
    assert PARSED_WEBPAGE_DOC == record
