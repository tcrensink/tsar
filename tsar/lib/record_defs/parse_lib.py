"""
library of parsing functions and utilities used by record_defs.

All file handling should be done from host machine via ssh.
Environment variables $HOME, $USER defined to match host in tsar/__init__.py
for pathlib handling.
"""
import os
import nltk
import pandas as pd
from collections import Counter
import numpy as np
from stat import S_ISDIR, S_ISREG

# from pathlib import Path
from datetime import datetime
from tsar.lib.ssh_utils import SSHClient


def resolve_path(path_str, sftp_client=None):
    """Attempt to generate canonical path from path string.

    Examples:
    ~/test ->               /Users/trensink/test
    ./test ->               /Users/trensink/test
    /Users/trensink/test -> /Users/trensink/test
    ../trensink/test ->     /Users/trensink/test
    """
    if not sftp_client:
        sftp_client = SSHClient().open_sftp()
    home_folder = os.environ["HOST_HOME"]
    sftp_client.chdir(home_folder)

    if path_str.startswith("~"):
        path_str = path_str.replace("~", home_folder, 1)
    path_str = sftp_client.normalize(path_str)
    return path_str


def return_file_contents(path_string, sftp_client=None):
    """Return string of file contents on remote host.

    e.g.: path_string = "~/test.py" -> string of file contents.
    """
    if not sftp_client:
        sftp_client = SSHClient().open_sftp()
    contents = sftp_client.file(path_string)
    contents_str = contents.read().decode()
    return contents_str


def list_folder_contents(path_string, sftp_client=None):
    """Return contents of longest valid folder on host.

    E.g.,  ./git/xxxx -> <list of files in ./git>
    """
    path_string = resolve_path(path_string, sftp_client)
    if not sftp_client:
        sftp_client = SSHClient().open_sftp()

    try:
        contents_list = sftp_client.listdir(path_string)
    except FileNotFoundError:
        contents_list = sftp_client.listdir(path_string.rsplit("/", 1)[0])
    return contents_list


def return_files(folder, extensions=None, sftp_client=None):
    """Return list of files in folder with extension."""
    if isinstance(extensions, str):
        extensions = [extensions]
    for extension in extensions:
        if not extension.startswith("."):
            raise ValueError("valid extensions start with a '.'")
    extensions = set([ex.rsplit(".", 1)[1] for ex in extensions])

    if not sftp_client:
        sftp_client = SSHClient().open_sftp()

    # recursively walk through folders to get all files with extension
    folder = resolve_path(folder, sftp_client)
    files = []

    def get_files(folder, files=files):

        folder_contents = sftp_client.listdir_attr(folder)
        for entry in folder_contents:
            mode = entry.st_mode
            fname = os.path.join(folder, entry.filename).lower()
            if S_ISDIR(mode):
                get_files(fname)
            elif S_ISREG(mode):
                file_ext = fname.split(".", 1)[-1]
                if extensions is None or file_ext in extensions:
                    files.append(fname)

    get_files(folder)
    return files


def open_textfile(path, editor, ssh_client=None):
    """Open text file with editor."""
    if not ssh_client:
        ssh_client = SSHClient()
    cmd = f"{editor} {path}"
    ssh_client.exec_command(cmd)


def open_url(url, browser, ssh_client=None):
    """Open url in browser."""
    if not ssh_client:
        ssh_client = SSHClient()
    cmd = f"open -a {browser} {url}"
    ssh_client.exec_command(cmd)


def file_base_features(path, record_type):
    """Return values for BASE_SCHEMA features."""

    base_feature_dict = {
        "record_id": path,
        "record_type": record_type,
        # "utc_last_access": os.stat(path).st_atime,
        "utc_last_access": 1600000000.0,
    }
    return base_feature_dict


def basic_text_to_keyword(raw_text, N):
    """Simple function to return keywords based on text of single doc.

    tokenizes, filters to alphabetical, top N scoring sqrt(freq)*word_length
    """
    words = raw_text.split()
    # words = nltk.word_tokenize(raw_text)
    words = [word.lower() for word in words if word.isalpha()]
    word_counts = dict(Counter(words))
    df = pd.DataFrame.from_dict(word_counts, columns=["count"], orient="index")
    df["length"] = df.index.str.len()
    df["importance"] = np.sqrt(df["count"]) * df["length"]
    keywords = set(df.nlargest(N, columns="importance").index)
    return keywords


def file_meta_data(path):
    """get file meta data.

    descr:
    st_atime: last access time (utc)
    st_mtime: last edit time (utc)
    st_size: in bytes
    st_ctime: last change to file metadata
    """
    # info = os.stat(path)
    info_dict = {
        "st_atime": 1600000000.0,
        "st_mtime": 1600000000.0,
        "st_ctime": 1600000000.0,
        "st_size": 1600000000.0,
        # "st_atime": info.st_atime,
        # "st_mtime": info.st_mtime,
        # "st_ctime": info.st_ctime,
        # "st_size": info.st_size,
    }
    return info_dict


def utc_now_timestamp():
    """Return utc timestamp for right now."""
    ts = datetime.utcnow().timestamp()
    return ts
