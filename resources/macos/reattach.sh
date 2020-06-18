# /bin/bash
docker attach tsar_run --detach-keys="ctrl-c"
# see: https://tldp.org/HOWTO/Keyboard-and-Console-HOWTO-4.html
echo -e \\033c
