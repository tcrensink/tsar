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
import sys
import pkg_resources

PLATFORM = sys.platform
APP_DIR = os.path.dirname(os.path.realpath(__file__))
KEY_FILE = "tsar_id_rsa"
KEY_FOLDER = os.path.expanduser("~/.ssh")
AUTHORIZED_KEYS_FILE = os.path.join(KEY_FOLDER, "authorized_keys")
GEN_KEYS = 'ssh-keygen -f {} -t rsa -b 4096'.format(KEY_FILE)
CPY_TO_AUTHORIZED_KEYS = 'cat ~/.ssh/{}.pub >> {}'.format(KEY_FILE, AUTHORIZED_KEYS_FILE)
ADD_PRIVATE_KEY_TO_AGENT = "ssh-add {}".format(KEY_FILE)
START_SSH_AGENT = 'eval "$(ssh-agent -s)"'
EXEC_PATH = "/usr/local/bin/tsar"
ADD_EXEC_TO_PATH = "sudo ln -sf {}/run.sh {} ".format(APP_DIR, EXEC_PATH)
ES_FOLDER = os.path.join(APP_DIR, "resources/elasticsearch")
ES_LOG_PATH = os.path.join(ES_FOLDER, "logs")
ES_DATA_PATH = os.path.join(ES_FOLDER, "data")
ES_CONFIG_TEMPLATE = os.path.join(ES_FOLDER, "elasticsearch.yml_template")
ES_CONFIG_PATH = os.path.join(ES_FOLDER, "elasticsearch.yml")


def install_macos():
    print("\n**Enable remote login:**\nNavigate to System Preferences -> Sharing, check `remote log in`")
    _ = input("Press return when complete:")

    _ = input(f"Install python dependencies in host_requirements.txt? (press return):")
    subprocess.call("python -m pip install -r host_requirements.txt", shell=True)

    print("generating key pairs {} in {}...".format(KEY_FILE, KEY_FOLDER))
    if not os.path.exists(KEY_FOLDER):
        os.mkdir(KEY_FOLDER)
    os.chdir(KEY_FOLDER)
    subprocess.call(GEN_KEYS, shell=True)

    print("\nAdding public key to authorized_keys and private key to ssh-agent via ssh-add...")
    subprocess.call(START_SSH_AGENT, shell=True)
    subprocess.call(CPY_TO_AUTHORIZED_KEYS, shell=True)
    subprocess.call(ADD_PRIVATE_KEY_TO_AGENT, shell=True)

    print("\nEnter user password to add file to path: {}".format(EXEC_PATH))
    subprocess.call(ADD_EXEC_TO_PATH, shell=True)

    print("\nupdating path references in elasticsearch.yml file...")
    with open(ES_CONFIG_TEMPLATE, mode='r') as fp:
        lines = fp.readlines()
    with open(ES_CONFIG_PATH, mode='w') as fp:
        for line_no, line in enumerate(lines):
            if line.startswith("path.data: "):
                new_line = "path.data: {}\n".format(ES_DATA_PATH)
                lines[line_no] = new_line
                print("replaced {} with {}".format(repr(line), repr(new_line)))
            elif line.startswith("path.logs: "):
                new_line = "path.logs: {}\n".format(ES_LOG_PATH)
                lines[line_no] = new_line
                print("replaced {} with {}".format(repr(line), repr(new_line)))
        fp.writelines(lines)

def install_linux():
    pass

if __name__ == "__main__":

    if PLATFORM.lower() == "darwin":
        install_macos()        
    
    else:
        raise NotImplementedError("Installation not currently supported for platform: {}".format(PLATFORM))

    print("\nSetup complete!\n")
