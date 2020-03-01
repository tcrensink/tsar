"""
library of parsing functions and utilities used by record_defs
"""
import subprocess
import os
from tsar.lib.record_def import BASE_SCHEMA
import nltk
import pandas as pd
from collections import Counter
import numpy as np
from pathlib import Path


def return_files(folder, extensions=None):
    """Return all files within folder for the given extension types."""
    if isinstance(extensions, str):
        raise TypeError("extensions should be a list, tuple, or set.")

    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise ValueError("a folder is needed to generate records.")

    paths = []
    for root, dirs, files in os.walk(folder):
        curr_paths = [resolve_path(os.path.join(root, f)) for f in files]
        if extensions:
            curr_paths = \
                [str(p) for p in curr_paths if p.suffix in set(extensions)]
        else:
            curr_paths = [str(p) for p in curr_paths]
        paths.extend(curr_paths)

    return paths


def resolve_path(path):
    """Resolve path, including relative, tilde, and env vars."""
    resolved_path = Path(path).resolve()
    return resolved_path


def open_textfile(path, editor):
    """Open text file with editor.
    -w returns to host program on close.
    """
    cmd = f"{editor} -w {path}"
    subprocess.Popen(cmd, shell=True).wait()


def return_raw_doc(path):
    """Return text doc as a string."""
    with open(path, 'r') as fp:
        text = fp.read()
    return text


def file_base_features(path, record_type):
    """Return values for BASE_SCHEMA features."""

    base_feature_dict = {
        "record_id": path,
        "record_type": record_type,
        "utc_last_access": os.stat(path).st_atime
    }
    return base_feature_dict


def basic_text_to_keyword(raw_text, N):
    """Simple function to return keywords based on text of single doc.

    tokenizes, filters to alphabetical, top N scoring sqrt(freq)*word_length
    """
    words = nltk.word_tokenize(raw_text)
    words=[word.lower() for word in words if word.isalpha()]
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
    info = os.stat(path)
    info_dict = {
        "st_atime": info.st_atime,
        "st_mtime": info.st_mtime,
        "st_ctime": info.st_ctime,
        "st_size": info.st_size
    }
    return info_dict
