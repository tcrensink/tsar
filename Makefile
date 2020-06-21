# network=host allows host/container to share network
# use `host.docker.internal` to connect from container -> host on mac
# rm: clean up docker image on exit
# -it creates interactive (pseudo) tty shell
# see also: reattach_shell.sh in ./resources

build:
	docker build --network=host -t tsar .

# rebuild, start shell in container
shell:
	docker run \
		--name tsar_shell \
		-e HOST_USER=${USER} \
		--rm \
		-it \
		--volume="$(shell pwd):/opt:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		--detach-keys="ctrl-c" \
		tsar \
		bash

# rebuild, run app in container
run:
	docker run \
		--name tsar \
		-e HOST_USER=${USER} \
		--rm \
		-itd \
		--volume="$(shell pwd):/opt:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		--detach-keys="ctrl-c" \
		tsar \
		bash
