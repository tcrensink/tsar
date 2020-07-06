# /bin/bash
NAME='tsar'
TSAR_PATH="$(pwd)"

# start "run" container if not running already
[[ $(docker ps -f "name=$NAME" --format '{{.Names}}') == $NAME ]] ||
(cd $TSAR_PATH && make run)

docker attach tsar --detach-keys="ctrl-v"
# see: https://tldp.org/HOWTO/Keyboard-and-Console-HOWTO-4.html
echo -e \\033c
