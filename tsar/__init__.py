"""
paths
"""
import os
# import sys

MODULE_PATH = __path__[0]
REPO_PATH = os.path.split(MODULE_PATH)[0]
COLLECTIONS_FOLDER = os.path.join(REPO_PATH, 'resources/collections/')
# CONTENT_FOLDER = os.path.join(REPO_PATH, 'tsar_content')

# _TEMP_METADB_PATH = METADB_PATH
_TEMP_CONTENT_FOLDER = os.path.join(REPO_PATH, '.tmp_content')

TESTS_FOLDER = os.path.join(REPO_PATH, "tests")