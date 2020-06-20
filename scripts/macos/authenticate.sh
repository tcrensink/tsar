#! /bin/bash

# this script enables ssh connection between the docker container and the host computer; to be run in docker container.

# paths in docker container
KEY_FOLDER="/opt/.ssh"
KEY_PATH="$KEY_FOLDER/id_rsa"

# create private/public key pair in shared, mounted folder
mkdir -p $KEY_FOLDER
ssh-keygen -t rsa -b 4096 -C "TSAR" -f $KEY_PATH
eval "$(ssh-agent -s)"
ssh-add $KEY_PATH

# add key to remote host (host routing for macos).  $HOST_USER defined in Makefile
ssh-copy-id $HOST_USER@host.docker.internal

# add host to known_hosts file
ssh-keyscan -H host.docker.internal >> /root/.ssh/known_hosts
