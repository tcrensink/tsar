"""
library of parsing functions and utilities.

"""
import os
from collections import Counter
import numpy as np
import pandas as pd
import re
import sys
from stat import S_ISDIR, S_ISREG
from datetime import datetime

import fsspec
from requests.utils import urlparse, urlunparse
from os import path

# host fileserver root
ROOT_DIR = os.environ.get("HOST_HOME")

FILE_HOST_PORT = 8139
# file system client; get folder contents at server ROOT_DIR
fs = fsspec.filesystem(protocol="http")


def url_to_host_path(path_url):
    """Convert url to (absolute) host path"""
    url_path = urlparse(path_url).path
    rel_path = url_path.lstrip("/")
    host_path = os.path.join(ROOT_DIR, rel_path)
    return host_path


def host_path_to_url(host_path):
    """Formats host (absolute) path to url"""
    host_path = resolve_path(host_path)
    rel_path = os.path.relpath(host_path, ROOT_DIR)
    url = urlunparse(
        ("http", f"host.docker.internal:{FILE_HOST_PORT}", rel_path, None, None, None)
    )
    return url


def exists_on_fs(path_url, fs=fs):
    # does the file/folder path url exist on the (host) file server?
    return fs.exists(path_url)


def return_links(text):
    """Return markdown-formatted links in text body."""
    links = re.findall(r"\[[^\]]+\]\(<?([^)<>]+)>?\)", text)
    return sorted(list(set(links)))


def resolve_path(path_str, source_path=None):
    """Resolve file paths to absolute path.

    - paths are identical in host, container
    - if source_path is specified, relative paths (./ ../) in path_str resolved
    relative to source_path
    """
    home_folder = os.environ["HOST_HOME"]
    path_str = path_str.replace("~", home_folder, 1)
    if source_path:
        source_dir = os.path.dirname(resolve_path(source_path))
        path_str = os.path.join(source_dir, path_str)

    path_str = os.path.abspath(path_str)
    return path_str


def return_file_contents(path_string, fs=fs):
    """Return string of file contents on remote host.

    e.g.: path_string = "~/test.py" -> string of file contents.
    """
    file_url = host_path_to_url(path_string)
    with fs.open(file_url, "r") as fp:
        contents_str = fp.read()
    return contents_str


def return_files(path, fs=fs, extensions=[]):
    """Return list of files in folder with extension.

    All input/output format as local (host) filepaths, not fs urls.
    """
    extensions = set([ex.rsplit(".", 1)[-1] for ex in extensions])

    # recursively walk through folders to get all files with extension
    path_url = host_path_to_url(path)

    files = []
    # bug: fs.isfile(url) returns True for dirs
    isfile = bool(not fs.isdir(path_url) and fs.exists(path_url))
    if isfile:
        files.append(path)
    elif fs.isdir(path_url):
        for dirpath, dirnames, filenames in fs.walk(path_url):
            curr_files = [
                os.path.join(url_to_host_path(dirpath), fn) for fn in filenames
            ]
            if extensions:
                curr_files = [
                    fn for fn in curr_files if fn.split(".")[-1] in extensions
                ]
            else:
                curr_files = [fn for fn in curr_files if fn.split(".")[-1]]
            files.extend(curr_files)
    else:
        raise ValueError(f"{path} not found; unable to proceed.")
    return files


def return_local_files(path, extensions=[]):
    """Return list of files in folder with extension."""
    extensions = set([ex.rsplit(".", 1)[-1] for ex in extensions])

    # recursively walk through folders to get all files with extension
    path = resolve_path(path)

    files = []
    if os.path.isfile(path):
        files.append(path)
    elif os.path.isdir(path):
        for dirpath, dirnames, filenames in os.walk(path):
            curr_files = [os.path.join(dirpath, fn) for fn in filenames]
            if extensions:
                curr_files = [
                    fn for fn in curr_files if fn.split(".")[-1] in extensions
                ]
            else:
                curr_files = [fn for fn in curr_files if fn.split(".")[-1]]
            files.extend(curr_files)
    else:
        raise ValueError(f"{path} not found; unable to proceed.")
    return files


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
    words = [word.lower() for word in words if word.isalpha()]
    word_counts = pd.Series(Counter(words))
    word_length = word_counts.index.str.len()
    # heuristic for gauging import words: long and frequently occuring
    word_importance = word_length * word_counts
    keywords = sorted(
        list(word_importance.nlargest(N).sort_values(ascending=False).index)
    )
    return keywords


def text_to_keyword_linked_doc(doc_text, link_texts, N, weight=0.65):
    """Simple function to return keywords for main doc including (weighting of) linked texts."""
    # main text:
    words = doc_text.split()
    words = [word.lower() for word in words if word.isalpha()]
    df = pd.DataFrame.from_dict(data=Counter(words), orient="index", columns=["counts"])
    df["doc_word_weight"] = df.index.str.len() * df["counts"]

    link_text = "\n".join(link_texts).split()
    link_words = [word.lower() for word in link_text if word.isalpha()]
    df_links = pd.DataFrame.from_dict(
        data=Counter(link_words), orient="index", columns=["counts"]
    )
    df_links["link_word_weight"] = df_links.index.str.len() * df_links["counts"]
    df = pd.merge(
        left=df_links[["link_word_weight"]],
        right=df[["doc_word_weight"]],
        how="outer",
        left_index=True,
        right_index=True,
    )
    df = df.fillna(0)
    word_weights = df["doc_word_weight"] + weight * df["link_word_weight"]
    keywords = list(word_weights.nlargest(N).sort_values(ascending=False).index)
    return keywords


def file_meta_data(path):
    """get file meta data.

    descr:
    st_atime: last access time (utc)
    st_mtime: last edit time (utc)
    st_size: in bytes
    st_ctime: last change to file metadata
    """
    info = os.stat(path)
    info_dict = {
        "st_atime": info.st_atime,
        "st_mtime": info.st_mtime,
        "st_ctime": info.st_ctime,
        "st_size": info.st_size,
    }
    return info_dict


def utc_now_timestamp():
    """Return utc timestamp for right now."""
    ts = datetime.utcnow().timestamp()
    return ts
