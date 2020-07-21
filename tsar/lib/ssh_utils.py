"""
Host connection utilities.

This module includes functionality for managing host-machine connection.  

Notes:
- Paramiko is significantly slower than comparable file operations on a mounted drive.
- This module includes duplicates of local functions found in parse_lib.py
"""
import os
import time
import subprocess
import paramiko

USER = os.environ["HOST_USER"]
HOST_KEY_FILE = "/root/.ssh/known_hosts"
HOSTNAME = "host.docker.internal"


class SSHClient(paramiko.SSHClient):
    """SSH client for connecting to the docker or other remote hosts."""

    def __init__(
        self, user=USER, hostname=HOSTNAME, host_key_file=HOST_KEY_FILE, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.load_host_keys(host_key_file)
        self.connect(username=user, hostname=hostname, banner_timeout=2000)

        # prevents connection from closing:
        channel = self.invoke_shell()
        channel.keep_this = self
        # return channel


def resolve_path(path_str, sftp_client=None):
    """Generate canonical path from path string.

    All paths assumed relative to $HOME. Expected behavior:
    ~/test ->               /Users/username/test
    ./test ->               /Users/username/test
    /Users/username/test -> /Users/username/test
    ../username/test ->     /Users/username/test
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
