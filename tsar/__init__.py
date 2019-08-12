"""
helper functions
"""
import os
# import sys

MODULE_PATH = __path__[0]
REPO_PATH = os.path.split(MODULE_PATH)[0]
METADB_PATH = os.path.join(REPO_PATH, 'tsar_dbs')
CONTENT_FOLDER = os.path.join(REPO_PATH, 'tsar_content')

_TEMP_CONTENT_FOLDER = os.path.join(CONTENT_FOLDER, '.tmp_content')
