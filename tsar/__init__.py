"""
paths
"""
import os

# all paths as seen on CONTAINER:
MODULE_PATH = __path__[0]
REPO_PATH = os.path.split(MODULE_PATH)[0]
RESOURCES_PATH = os.path.join(REPO_PATH, "resources/")
COLLECTIONS_FOLDER = os.path.join(RESOURCES_PATH, "collections/")
# CONTENT_FOLDER = os.path.join(REPO_PATH, 'tsar_content')
CAPTURE_DOC_PATH = os.path.join(RESOURCES_PATH, "capture.md")

# _TEMP_METADB_PATH = METADB_PATH
_TEMP_CONTENT_FOLDER = os.path.join(REPO_PATH, ".tmp_content")
TESTS_FOLDER = os.path.join(REPO_PATH, "tests")


# All paths as seen on HOST machine
HOST_REPO_PATH = os.environ["HOST_DIR"]
# HOST_REPO_PATH = os.path.split(HOST_MODULE_PATH)[0]
HOST_RESOURCES_PATH = os.path.join(HOST_REPO_PATH, "resources/")
HOST_TESTS_FOLDER = os.path.join(HOST_REPO_PATH, "tests")

del os
