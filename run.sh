#! /bin/bash
NAME='tsar'
# get directory of repo, following symlinks
TSAR_PATH="$(dirname "$(readlink -f "$0")")"

# start "run" container if not running already
[[ $(docker ps -f "name=$NAME" --format '{{.Names}}') == $NAME ]] ||
(cd $TSAR_PATH && make run)

docker attach tsar --detach-keys="ctrl-v"
# see: https://tldp.org/HOWTO/Keyboard-and-Console-HOWTO-4.html
echo -e \\033c
