#! python
"""
This file to contain all (one-time) install modifications for all supported platforms.  Specifically:

**** SET UP SSH AUTHENTICATION FROM DOCKER CONTAINER -> HOST ****
    - generate key pair on host
    - add public key to authorized_keys file (on host)
    - add private key to ssh-agent (on host)
    - *ssh-agent with private key is forwarded to container in docker run.

**** CREATE ALIAS ****
    - create softlink tsar -> run.sh on $PATH

**** BUILD DOCKER CONTAINER ****

resources:
- https://docs.github.com/en/github/authenticating-to-github/about-ssh
"""
from builtins import input
import subprocess
import os

APP_DIR = os.path.dirname(os.path.realpath(__file__))
KEY_FILE = "tsar_id_rsa"
KEY_FOLDER = os.path.expanduser("~/.ssh")
AUTHORIZED_KEYS_FILE = os.path.join(KEY_FOLDER, "authorized_keys")
GEN_KEYS = 'ssh-keygen -f {} -t rsa -b 4096'.format(KEY_FILE)
CPY_TO_AUTHORIZED_KEYS = 'cat ~/.ssh/{}.pub >> {}'.format(KEY_FILE, AUTHORIZED_KEYS_FILE)
ADD_PRIVATE_KEY_TO_AGENT = "ssh-add {}".format(KEY_FILE)

EXEC_NAME = "tsar"
ADD_EXEC_TO_PATH = "sudo ln -sf {}/run.sh /usr/local/bin/{} ".format(APP_DIR, EXEC_NAME)

ES_CONFIG_PATH = os.path.join(APP_DIR, "resources/elasticsearch/elasticsearch.yml")
ES_LOG_PATH = os.path.join(os.path.dirname(ES_CONFIG_PATH), "logs")
ES_DATA_PATH = os.path.join(os.path.dirname(ES_CONFIG_PATH), "data")

if __name__ == "__main__":

    print("macos: enable remote login. See System Preferences -> Sharing: check `remote log in`")
    _ = input("(press return when complete)")

    print("generating key pairs {} in {}...".format(KEY_FILE, KEY_FOLDER))
    if not os.path.exists(KEY_FOLDER):
        os.mkdir(KEY_FOLDER)
    os.chdir(KEY_FOLDER)
    subprocess.call(GEN_KEYS, shell=True)

    print("adding public key to authorized_keys and private key to ssh-agent via ssh-add...")
    subprocess.call(CPY_TO_AUTHORIZED_KEYS, shell=True)
    subprocess.call(ADD_PRIVATE_KEY_TO_AGENT, shell=True)

    print("Add executable to $PATH (user password needed)...")
    subprocess.call(ADD_EXEC_TO_PATH, shell=True)

    print("updating path references in elasticsearch.yml file...")
    with open(ES_CONFIG_PATH, mode='r') as fp:
        lines = fp.readlines()
    with open(ES_CONFIG_PATH, mode='w') as fp:
        for line_no, line in enumerate(lines):
            if line.startswith("path.data: "):
                new_line = f"path.data: {ES_DATA_PATH}\n"
                lines[line_no] = new_line
                print(f"replaced {repr(line)} with {repr(new_line)}")
            elif line.startswith("path.logs: "):
                new_line = f"path.logs: {ES_LOG_PATH}\n"
                lines[line_no] = new_line
                print(f"replaced {repr(line)} with {repr(new_line)}")
        fp.writelines(lines)



    print("\nsetup complete!\n")
