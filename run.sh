#! /bin/bash

# run.sh used for faster connection than run.py
tsar_folder="$(dirname "$(readlink "$0")")"
container='tsar'
nargs="$#"

# if tsar is not running, start it
if ! [ "$(docker ps -f "name=$container" --format '{{.Names}}')" = "$container" ]; then
echo "starting tsar..."
(cd $tsar_folder && docker compose up -d app)
fi

# if tsar already running, no args provided, attach to container
if [ $nargs -eq 0 ]; then
# echo "attaching to tsar; clear screen after detaching..."
docker attach "$container" --detach-keys="ctrl-c"
printf "\033c"
else
python3 "$tsar_folder/click_cli.py" $@
fi
