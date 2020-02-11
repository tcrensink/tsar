#!/Users/trensink/anaconda3/envs/tsar/bin/python
"""
This file is the tsar script that is called from the command line.

The App class initializes all objects needed for tsar (metadb, elasticsearch client, and file extractor).
self._parse_command_line_args(), and
executes an associated method (e.g. self.edit_tsar_file).
"""

import sys
import argparse
import os
import shutil
from tsar import (
    config,
    METADB_PATH,
    CONTENT_FOLDER,
    REPO_PATH,
    _TEMP_CONTENT_FOLDER,
    _TEMP_METADB_PATH
)
from pathlib import Path
from tsar.lib import (
    search,
    metadb,
    file_parser,
    io
)
from tsar.app import search_page
from datetime import datetime
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import PromptSession
DEFAULT_RECORD_TYPE = 'wiki'
DEFAULT_DB_PATH = os.path.join(METADB_PATH, 'tsar.pkl')
DEFAULT_SEARCH_INDEX = 'wiki'

# "inspecting" a folder uses temporary index, db, content folder:
_TEMP_SEARCH_INDEX = 'temp_index'
_TEMP_DB_PATH = os.path.join(_TEMP_METADB_PATH, '.tmp.pkl')


class App(object):

    def __init__(
        self,
        record_type=DEFAULT_RECORD_TYPE,
        db_path=DEFAULT_DB_PATH,
        index=DEFAULT_SEARCH_INDEX,
        content_folder=CONTENT_FOLDER
    ):
        """initialize:
        - search client (and specific index)
        - extractor (file -> metadata)
        - tsar_db (metadata db)
        """
        try:
            search.test_server()
        except Exception:
            search.launch_es_daemon()

        self.record_type = record_type
        self.db_path = db_path
        self.index = index
        self.content_folder = content_folder

        self.tsar_db = metadb.TsarDB(self.db_path)
        self.extractor = file_parser.Extractor(self.record_type)
        self.tsar_search = search.TsarSearch()

    def main(self):
        """The main function that runs the command line supplied command, args, kwargs.
        """
        # process command input
        (func, kwargs) = self._parse_command_line_args()

        print('executing command: `{}`'.format(func.__name__))
        func(**kwargs)
        print('exiting tsar')

    def _parse_command_line_args(self):
        """command line argument parser.  Each command has its own argument parser,
        and refers to a method by the same name.

        - each separate command uses a subparser to parse the arguments
        """
        parser = argparse.ArgumentParser(prog='tsar', description='tsar: the textual search and retrieve engine.  Use one of the following commands:')
        subparsers = parser.add_subparsers()

        parser_init = subparsers.add_parser('init', help='initialize a new tsar db from files in contents folder.')
        parser_init.set_defaults(func=self.initialize_tsar)
        parser_edit = subparsers.add_parser('edit', help='open file (new or existing) in contents folder (and generate metadata)')
        parser_edit.add_argument('fname', nargs='?', default=None)
        parser_edit.set_defaults(func=self.edit_tsar_file)
        parser_search = subparsers.add_parser('query', help="""
            interactively search records: enter number to open corresponding file, q to quit.
            """)
        parser_search.set_defaults(func=self.search_records)
        parser_add_new_files = subparsers.add_parser('add', help='add existing files to tsar content folder (and generate metadata)')
        parser_add_new_files.add_argument('source_path', nargs=1, default=None)
        parser_add_new_files.set_defaults(func=self.add_tsar_files)
        parser_inspect = subparsers.add_parser('inspect', help='search folder contents without creating a permanent tsar repo.')
        parser_inspect.add_argument('source_path', nargs=1, default=None)
        parser_inspect.set_defaults(func=self.inspect_folder)

        parser_rm = subparsers.add_parser('rm', help='delete all contents from content folder and associted metadata.')
        parser_rm.set_defaults(func=self.rm_tsar)

        args = parser.parse_args()

        kwargs = vars(args)
        try:
            func = kwargs.pop('func')
        except KeyError:
            parser.print_help()
            sys.exit(0)
            # func = self.search_records
            # func = self.edit_tsar_file
        return (func, kwargs)


    def rm_tsar(self):
        """remove all tsar content and metadata
        """
        print('to be implemented...')


    def search_records(self):
        """open prompt-toolkit interface for searching/returning records
        """
        search_page.run(self)


    def edit_tsar_file(self, fname=None):
        """edit existing (or create new) tsar file in the tsar_content directory

        Given a name, edit a file and create a new associated tsar record.
        """
        if self.tsar_db.df is None:
            raise FileNotFoundError('\nNo database found at {} \nCreate a new db for contents in {} with `tsar init`'.format(self.content_folder, self.db_path))
        if fname is None:
            date_str = datetime.utcnow().isoformat(sep='_', timespec='seconds')
            fname = '-'.join(date_str.split(':')) + '.md'
        else:
            fname = fname

        # open path in editor
        file_path = os.path.join(CONTENT_FOLDER, fname)
        io.open_record(file_path)
        # update record, index if file exists (may not have been saved):
        if os.path.exists(file_path):
            self._update_record(file_path)

    def initialize_tsar(self):
        """reset metadata and index for tsar content
        - (leave content alone)
        - remove metadata if it exists
        - recreates tsardb from content
        - recreate index from tsardb
        - exit with note to user (successful?)
        """
        # remove db & search index
        self.tsar_db.remove_db()
        self.tsar_db.create_db(schema=self.extractor.schema)
        self.tsar_search.delete_index()
        self.tsar_search.create_index()
        # get relevant files
        if not os.path.exists(self.content_folder):
            os.mkdir(self.content_folder)
        file_paths = file_parser.get_valid_files(self.content_folder, self.extractor.file_extensions)
        # generate records, index for each file
        for path in file_paths:
            self._update_record(path, write_db=False)
        self.tsar_db.write_db()
        print('finished generating tsar from {}'.format(self.content_folder))

    def _update_record(self, path, write_db=True):
        """for record associated with path,
        - update record in db
        - update record_id in index
        """
        record = self.extractor.generate_record(path)
        record_id = record[self.extractor.record_id_field]
        record_type = record['record_type']
        self.tsar_db.update_record(
            record=record,
            record_id=record_id
        )
        self.tsar_search.index_record(
            record,
            record_id,
            record_type
        )
        if write_db:
            self.tsar_db.write_db()

    def _add_file(
        self,
        source_path,
        overwrite_existing=False,
        update_record=True,
        write_db=True,
        fname=None,
        softlink=True
    ):
        """add an existing file (not currently in tsar) to tsar_content folder:

        - check that file can successfully be parsed
        - if so, copy file to self.content_folder/name
        - optionally update (add) the record in tsar_db
        - optionally write_db (set to False if adding several files, write once when finished)
        - returns new path in tsar_content folder if created

        Alternatives to interacting with files in wider filesystem include softlink/hardlink into content_folder, or merely generating metadata without touching source folders.
        """
        if fname is None:
            fname = file_parser.to_Path(source_path).name
        tsar_path = os.path.join(self.content_folder, fname)

        # generate softlink or create hard copies
        if softlink:
            cp_fun = os.symlink
        else:
            cp_fun = shutil.copy2

        already_exists = os.path.exists(tsar_path)
        if (overwrite_existing is False) and (already_exists is True):
            print('file already file already exists: {}'.format(source_path))
            return None

        # try generating record first; if successful, copy file to content_folder and generate record
        try:
            _ = self.extractor.generate_record(source_path)
            cp_fun(source_path, tsar_path)
            if update_record:
                self._update_record(tsar_path, write_db=write_db)
        except:
            print('error creating record from {}'.format(source_path))
            return None
        return tsar_path

    def add_tsar_files(
        self,
        source_path,
        overwrite_existing=False,
        update_record=True,
        write_db=False,
        fname=None,
        softlink=False,
    ):
        """add a file or folder by copying contents to contents_folder, and updating records

        - if file, accepts fname argument
        - if folder, default (source file name) is used for contents
        """
        source_path = str(file_parser.to_Path(source_path[0]))
        # generate list of source_paths, enforce default fname if folder
        source_paths = []
        if os.path.isfile(source_path):
            source_paths.append(source_path)
        elif os.path.isdir(source_path):
            source_paths = file_parser.get_valid_files(source_path, self.extractor.file_extensions)
        else:
            raise NameError('{} is neither a file nor folder'.format(source_path))

        for source_path in source_paths:
            self._add_file(
                source_path=source_path,
                overwrite_existing=overwrite_existing,
                update_record=update_record,
                write_db=write_db,
                fname=fname,
                softlink=softlink,
            )
        self.tsar_db.write_db()
        print('added {} record(s) from {}'.format(len(source_paths), source_path))

    def inspect_folder(
        self,
        source_path,
        record_type=DEFAULT_RECORD_TYPE,
        ):
        """create a temporary tsar instance for examining folder contents, remove db, index afterwards

        - remap attributes to temp vars
        - initialize with tmp vars (re)write metadata, index, etc.
        - symlink files into temp directory
        - initialize tsar from temp directory (create new db, index, generate records)
        - run interactive search
        - clean up (delete index, db, files)
        """
        # reinit temp vars:
        self.db_path = _TEMP_DB_PATH
        self.index = _TEMP_SEARCH_INDEX
        self.content_folder = _TEMP_CONTENT_FOLDER
        self.record_type = record_type
        self.tsar_db = metadb.TsarDB(self.db_path)
        self.extractor = file_parser.Extractor(self.record_type)
        self.tsar_search = search.TsarSearch(index=self.index)
        # recreate blank tmp db, index
        print('generating db and index...')
        self.initialize_tsar()

        self.add_tsar_files(
            source_path,
            overwrite_existing=False,
            update_record=True,
            write_db=True,
            fname=None,
            softlink=True,
        )
        self.search_records()


if __name__ == '__main__':

    app = App()
    app.main()
