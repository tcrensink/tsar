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
		--name tsar \
		-e HOST_USER=${USER} \
		--rm \
		-it \
		--volume="$(shell pwd):/opt:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		--detach-keys="ctrl-c" \
		tsar \
		bash

shell: build shell_no_build

# rebuild, run app in container
dev_no_build:
	docker run \
		--name tsar_dev \
		-it \
		-e HOST_USER=${USER} \
		--rm \
		--volume="$(shell pwd):/opt" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		tsar \
		bash

dev: build dev_no_build
