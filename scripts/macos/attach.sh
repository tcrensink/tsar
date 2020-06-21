# /bin/bash
NAME='tsar'

# conditionally start container
[[ $(docker ps -f "name=$NAME" --format '{{.Names}}') == $NAME ]] ||
(cd ../../ && make run)

docker attach tsar --detach-keys="ctrl-c"
# see: https://tldp.org/HOWTO/Keyboard-and-Console-HOWTO-4.html
echo -e \\033c
