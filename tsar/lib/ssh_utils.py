"""
Host connection utilities.

This module includes functionality for managing host-machine connection
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
        self.connect(username=user, hostname=hostname, banner_timeout=200)

        # prevents connection from closing:
        channel = self.invoke_shell()
        channel.keep_this = self
        # return channel
