"""
package-wide import values
"""
import os
from tsar import doctypes
from tsar.doctypes.markdown_doc import MarkdownDoc
from tsar.doctypes.arxiv_doc import ArxivDoc

# list of recognized doc types
DOCTYPES = {
    ArxivDoc.__name__: ArxivDoc,
    MarkdownDoc.__name__: MarkdownDoc,
}

# all paths as seen on CONTAINER:
MODULE_PATH = __path__[0]
REPO_PATH = os.path.split(MODULE_PATH)[0]
RESOURCES_PATH = os.path.join(REPO_PATH, "resources/")
COLLECTIONS_FOLDER = os.path.join(RESOURCES_PATH, "collections/")
# CONTENT_FOLDER = os.path.join(REPO_PATH, 'tsar_content')
CAPTURE_DOC_PATH = os.path.join(RESOURCES_PATH, "capture.md")

LOG_PATH = os.path.join(RESOURCES_PATH, "tsar.log")

# _TEMP_METADB_PATH = METADB_PATH
_TEMP_CONTENT_FOLDER = os.path.join(REPO_PATH, ".tmp_content")
TESTS_FOLDER = os.path.join(REPO_PATH, "tests")
TEST_FIXTURES_FOLDER = os.path.join(REPO_PATH, "tests/fixtures")
TEST_RESOURCES_FOLDER = os.path.join(REPO_PATH, "tests/resources")


# All paths as seen on HOST machine (should now be mounted to same path in container)
HOST_HOME_FOLDER = os.environ["HOST_HOME"]
HOST_REPO_PATH = os.environ["HOST_DIR"]
# HOST_REPO_PATH = os.path.split(HOST_MODULE_PATH)[0]
HOST_RESOURCES_PATH = os.path.join(HOST_REPO_PATH, "resources/")
HOST_TESTS_FOLDER = os.path.join(HOST_REPO_PATH, "tests")

del os
