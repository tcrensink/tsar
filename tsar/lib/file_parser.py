"""
This file contains code to convert source files into records ready for ingestion by metadb.py

A "record_type" implies a specific file parser and schema; the Extractor class acts as an interface
for each specific record type implmentation that is itself record_type agnostic.

Todo:
- consolidate all associated information into
a "record_definition" (maybe one for each file?):
    - record_type (references all fields below)
    - record_schema (used by tsardb)
    - record_index (used by search, tsardb)
    - file_parser

record types and schemas (single nested dict, RECORD_DEFINITIONS?)

- consider using a parsing library for different file types if they exist.
- consider using ABC to define interface if several types are added
"""
import os
import numpy as np
import functools
from datetime import datetime
from pathlib import Path

"""
schema fields common to record types.  Some fields are used to generate file meta data
"""
COMMON_SCHEMA = {
    'record_type': str,
    'file_hash': int,
    'file_size': int,
    'file_creation_time': np.datetime64,
    'file_access_times': object,
    'file_path': str,
}

def return_record_definition(record_type):
    """return the record definition dict based on the record type name; these are set as attributes in Extractor.  Specifically:

    - record type
    - record id field
    - record hash field
    - record schema
    - record parser
    - associated file extensions
    """

    # generic record_dict:
    record_dict = {}
    record_dict['schema'] = COMMON_SCHEMA
    record_dict['record_type'] = record_type
    record_dict['record_id_field'] = 'file_path'

    # record-type specific modifications:
    if record_type == 'wiki':
        record_dict['schema'].update(
            {
                'content': str,
                'keywords': object
            }
        )
        record_dict['record_hash_field'] = 'content'
        record_dict['_parser'] = functools.partial(_parse_wiki, content_col='content', keyword_col='keywords')
        # only add files with these file extensions:
        record_dict['file_extensions'] = ('.md')

    return record_dict


class Extractor(object):
    """
    An interface for extracting record (dicts) from files given a specified record_type.

    - record_schema
    - file_parser
    - hash field (record content)
    - file metadata
    """

    def __init__(self, record_type):

        record_def = return_record_definition(record_type)
        for k, v in record_def.items():
            setattr(self, k, v)

    def parse_file(self, path):
        """parse file into a record of record_type, associated with the schema.
        """
        return self._parser(path)

    def file_meta_data(self, path):
        """generate meta data for a given file
        """
        meta_dict = return_file_meta_data(path)
        meta_dict['record_type'] = self.record_type
        return meta_dict

    def generate_record(self, path):
        """generate a record for a given file, including metadata and file hash
        """
        file_dict = self.parse_file(path)
        meta_dict = self.file_meta_data(path)
        hash_dict = {
            'file_hash': hash(file_dict[self.record_hash_field])
        }
        record_dict = {**file_dict, **meta_dict, **hash_dict}
        if len(record_dict) != len(self.schema):
            key_diff = set(record_dict.keys()).symmetric_difference(set(self.schema.keys()))
            raise KeyError('record does not match schema.  key mis-match: {}'.format(key_diff))

        return record_dict


def _parse_wiki(path, content_col, keyword_col):
    """return a dict of a parsed wiki page
    """
    with open(path, 'r') as fp:
        text = fp.read()

    parsed_data = {}
    parsed_data[content_col] = text

    keywords = set()
    for line in text.split('\n'):
        if line.startswith('#'):
            new = line.strip('#').strip().split(' ')
            keywords.update(new)
    parsed_data[keyword_col] = keywords
    return parsed_data


def return_file_meta_data(path):
    """get file-type independent meta data.

    - file_size
    - file_creation_time
    - file_access_times
    - record type
    """
    meta_dict = {}

    meta_dict['file_size'] = os.path.getsize(path)
    creation_time = datetime.fromtimestamp(os.path.getctime(path))
    meta_dict['file_creation_time'] = creation_time
    access_times = [datetime.fromtimestamp(os.path.getatime(path))]
    meta_dict['file_access_times'] = access_times
    meta_dict['file_path'] = path
    return meta_dict

def to_Path(path):
    """returns expanded path objct from a string.
    """
    expanded_path = Path(path).expanduser().resolve()
    return expanded_path

def get_valid_files(path, file_extensions):
    """Return list of all files in path that end with file_extensions.
    """
    path = to_Path(path)

    if not path.exists():
        raise FileNotFoundError('{} doesn\'t exist'.format(str(path)))

    if path.is_file() and (path.suffix in file_extensions):
        file_paths = [path]

    if path.is_dir():
        file_paths = []
        for currdir, subdir, fnames in os.walk(str(path)):
            file_exts = [os.path.splitext(fn)[1] for fn in fnames]
            fpaths = [os.path.join(currdir, fn) for fn in fnames]
            valid_fpaths = [fp for fp, ext in zip(fpaths, file_exts) if ext in file_extensions]
            file_paths.extend(valid_fpaths)
    return file_paths
