#! python
"""
This file to contain all (one-time) install modifications for all supported platforms:

# set up ssh authentication from docker container to host
# build docker container
# create executable and alias to tsar
# ...

resources:
- https://docs.github.com/en/github/authenticating-to-github/about-ssh
"""
import subprocess
import os

KEY_FILE = "tsar_id_rsa"
KEY_FOLDER = os.path.expanduser("~/.ssh")
AUTHORIZED_KEYS_FILE = os.path.join(KEY_FOLDER, "authorized_keys")
GEN_KEYS = 'ssh-keygen -f {} -t rsa -b 4096'.format(KEY_FILE)
CPY_TO_AUTHORIZED_KEYS = 'cat ~/.ssh/{}.pub >> {}'.format(KEY_FILE, AUTHORIZED_KEYS_FILE)
ADD_PRIVATE_KEY_TO_AGENT = "ssh-add {}".format(KEY_FILE)

if __name__ == "__main__":

    print("(macos) enable remote login: System Preferences -> Sharing: check `remote log in`")
    _ = input("(return to continue)")

    print("generating key pairs {} in {}...".format(KEY_FILE, KEY_FOLDER))
    if not os.path.exists(KEY_FOLDER):
        os.mkdir(KEY_FOLDER)
    os.chdir(KEY_FOLDER)
    subprocess.run(GEN_KEYS)

    print("adding public key to authorized_keys and private key to ssh-agent via ssh-add...")
    subprocess.run(CPY_TO_AUTHORIZED_KEYS)
    subprocess.run(ADD_PRIVATE_KEY_TO_AGENT)
