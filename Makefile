# network=host allows host/container to share network
# use `host.docker.internal` to connect from container -> host on mac
# rm: clean up docker image on exit
# -it creates interactive (pseudo) tty shell
# see also: reattach_shell.sh in ./resources

build:
	docker build --network=host -t tsar .

# rebuild, start shell in container
shell_no_build:
	docker run \
		--name tsar_shell \
		-e HOST_USER=${USER} \
		--rm \
		-it \
		--volume="$(shell pwd):/opt:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="3g" \
		--detach-keys="ctrl-q" \
		tsar \
		bash

shell: build shell_no_build

# rebuild, run app in container
run_no_build:
	docker run \
		--name tsar_run \
		-it \
		-e HOST_USER=${USER} \
		--rm \
		--volume="$(shell pwd):/opt" \
		--memory="3g" \
		--detach-keys="ctrl-c" \
		tsar \
		tsar

run: build run_no_build
