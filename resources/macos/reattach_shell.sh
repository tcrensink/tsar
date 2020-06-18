# /bin/bash
docker attach tsar_shell --detach-keys="ctrl-q"
# see: https://tldp.org/HOWTO/Keyboard-and-Console-HOWTO-4.html
echo -e \\033c
