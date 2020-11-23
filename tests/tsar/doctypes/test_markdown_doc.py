import os
import pytest
from tsar.doctypes.markdown_doc import MarkdownDoc
from tsar.doctypes.doctype import DocType
from tsar import TESTS_FOLDER, TEST_FIXTURES_FOLDER, TEST_RESOURCES_FOLDER
from tests.resources.parsed_docs import SOURCE1_MARKDOWN_DOC_RECORD

SOURCE_DOC1 = os.path.join(TEST_FIXTURES_FOLDER, "source_path1/source1_doc.md")


def test_subclass():
    assert issubclass(MarkdownDoc, DocType)
    assert isinstance(MarkdownDoc(), DocType)


def test_gen_record():
    """Verify record generation matches expected output."""
    record = MarkdownDoc.gen_record(SOURCE_DOC1, primary_doc=True, gen_links=True)
    assert SOURCE1_MARKDOWN_DOC_RECORD == record


def test_gen_links():
    """Test link generation."""
    record = MarkdownDoc.gen_record(SOURCE_DOC1, primary_doc=True, gen_links=True)
    links = sorted(MarkdownDoc.gen_links(record["content"]))
    assert links == sorted(
        ["../source_path2/source2_doc.md", "https://arxiv.org/abs/1906.03926"]
    )
