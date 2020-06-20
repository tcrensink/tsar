#! /bin/bash
# this script used for initial installation.

COMMAND='tsar'
FOLDER=$(pwd)

# build docker image
make build

# set up authentication: `docker exec -i mycontainer bash < mylocal.sh`


# create link to attach.sh in path: `ln -s executable attach.sh;
ln -s "$(pwd)/attach.sh" "/usr/bin/$COMMAND"