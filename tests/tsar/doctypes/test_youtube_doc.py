import os
import pytest
from tsar.doctypes.youtube_doc import YoutubeDoc
from tsar.doctypes.doctype import DocType
from tsar import TESTS_FOLDER, TEST_FIXTURES_FOLDER, TEST_RESOURCES_FOLDER
from tests.resources.parsed_docs import YOUTUBE_RECORD_aircAruvnKk

YOUTUBE_DOC_ID = "https://www.youtube.com/watch?v=aircAruvnKk"

MULTI_DOCTYPE_LINK_DOC = os.path.join(TEST_FIXTURES_FOLDER, "multi_doctype_link.md")


def test_subclass():
    assert issubclass(YoutubeDoc, DocType)
    assert isinstance(YoutubeDoc(), DocType)

def test_gen_record():
    """Verify record generation matches expected output."""
    record = YoutubeDoc.gen_record(YOUTUBE_DOC_ID, primary_doc=True, gen_links=True)
    assert YOUTUBE_RECORD_aircAruvnKk == record
