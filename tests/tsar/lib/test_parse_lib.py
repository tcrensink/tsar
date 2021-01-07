from tsar import HOST_TESTS_FOLDER, TESTS_FOLDER, TEST_FIXTURES_FOLDER, HOST_HOME_FOLDER, HOST_REPO_PATH
import os
import pytest
from tsar.lib import parse_lib

@pytest.fixture
def omni_file_text():
    with open(os.path.join(HOST_TESTS_FOLDER, "fixtures/omni_doc.md")) as fp:
        text = fp.read()
    return text

def test_resolve_path():
    """ Test that relative ~, ./ resolve correctly.  Paths are relative to os.getcwd()."""
    path1 = "~/test"
    path2 = "./test"
    target_path1 = os.path.join(HOST_HOME_FOLDER, "test")
    target_path2 = os.path.join(HOST_REPO_PATH, "test")
    assert parse_lib.resolve_path(path1) == target_path1
    assert parse_lib.resolve_path(path2) == target_path2


def test_resolve_path_relative():
    """Test that relative paths resolved correctly for [link](./relative_path.md)"""

    source_path = os.path.join(TEST_FIXTURES_FOLDER, "source_path1/source1_doc.md")
    test_path = "../source_path2/source2_doc.md"

    resolved_test_path = parse_lib.resolve_path(test_path, source_path=source_path)
    true_test_path = os.path.join(TEST_FIXTURES_FOLDER, "source_path2/source2_doc.md")
    assert resolved_test_path == true_test_path


def test_return_links(omni_file_text):
    links = parse_lib.return_links(omni_file_text)

    expected_links = [
        './wiki_docs/doc1.md',
        'https://arxiv.org/abs/1906.03926',
        'https://en.wikipedia.org/wiki/Le_Jour_des_fourmis',
    ]
    assert set(expected_links) == set(links)
