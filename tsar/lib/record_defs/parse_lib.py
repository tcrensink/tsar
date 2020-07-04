"""
library of parsing functions and utilities used by record_defs.

All file handling should be done from host machine via ssh.
Environment variables $HOME, $USER defined to match host in tsar/__init__.py
for pathlib handling.
"""
import subprocess
from subprocess import PIPE
import os
import nltk
import pandas as pd
from collections import Counter
import numpy as np

# from pathlib import Path
from datetime import datetime
from tsar.lib import ssh_utils

SSH_TO_HOST = "ssh {}@host.docker.internal".format(os.environ["HOST_USER"])

IS_FILE = "test -f {}"
IS_DIR = "test -d {}"


def return_file_contents(path_string, ssh_client=None):
    """Return string of file contents on remote host.

    e.g.: path_string = "~/test.py" -> string of file contents.
    """
    if not ssh_client:
        ssh_client = ssh_utils.SSHClient()
    cmd = f"cat {path_string}"
    _, stdout, _ = ssh_client.exec_command(cmd)
    listed_contents = stdout.read().decode()
    return listed_contents


def list_folder_contents(path_string, ssh_client=None):
    """Return string of folder contents on remote host.

    e.g.: path_string = "~/*.py" -> string with list of
    python files in home dir.
    """
    if not ssh_client:
        ssh_client = ssh_utils.SSHClient()
    cmd = f"ls -d1 {path_string}"
    _, stdout, _ = ssh_client.exec_command(cmd)
    listed_contents = stdout.read().decode()
    return listed_contents


def return_files(folder, extensions=None):
    """Return list of files in folder with extensions.

    Currently for macos only.
    """
    cmd = f"{SSH_TO_HOST} find {folder} -type f"

    if extensions:
        extensions = ["." + ext.lstrip(".") for ext in extensions]
        extensions_str = " -o ".join([f"-iname '\*{ext}'" for ext in extensions])
        cmd = f"{cmd} {extensions_str}"
    print(cmd)
    proc = subprocess.run(cmd, shell=True, stdout=PIPE)
    paths = proc.stdout.decode().splitlines()
    return paths


def open_textfile(path, editor):
    """Open text file with editor."""
    cmd = f"{SSH_TO_HOST} {editor} {path}".split(" ")
    subprocess.Popen(cmd)


def open_url(url, browser, ssh_client=None):
    """Open url in browser."""
    if not ssh_client:
        ssh_client = ssh_utils.SSHClient()
    cmd = f"open -a {browser} {url} && osascript -e 'tell application \"{browser}\" to activate'"
    ssh_client.exec_command(cmd)


def return_raw_doc(path):
    """Return text doc as a string."""
    cmd = f"{SSH_TO_HOST} test -f {path} && cat {path}"
    proc = subprocess.run(cmd, shell=True, stdout=PIPE)
    text = proc.stdout.decode()
    return text


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
