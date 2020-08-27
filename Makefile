# network=host allows host/container to share network
# use `host.docker.internal` to connect from container -> host on mac
# rm: clean up docker image on exit
# -it creates interactive (pseudo) tty shell
# see also: reattach_shell.sh in ./resources
SYSTEM = $(shell uname)

build:
	docker build \
		--network=host \
		-t tsar . \
		--build-arg tsar_folder=$(shell pwd)

# MACOS TARGETS
ifeq (${SYSTEM}, Darwin)

run: build
	docker run \
		-p 8137:8137 \
		--name tsar \
		-e HOST_USER=${USER} \
		-e HOST_DIR=$(shell pwd) \
		-e HOST_HOME=${HOME} \
		--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock \
		-e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock" \
		--rm \
		-idt \
		--volume="${HOME}:${HOME}:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		tsar \
		python "$(shell pwd)/tsar/app/app.py"

shell: build 
	docker run \
		-p 8137:8137 \
		--name tsar \
		-e HOST_USER=${USER} \
		-e HOST_DIR=$(shell pwd) \
		-e HOST_HOME=${HOME} \
		--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock \
		-e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock" \
		--rm \
		-it \
		--volume="${HOME}:${HOME}:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		--detach-keys="ctrl-q" \
		tsar \
		bash

# LINUX TARGETS
else ifeq (${SYSTEM}, LINUX)

run: build
	docker run \
		-p 8137:8137 \
		--name tsar \
		-e HOST_USER=${USER} \
		-e HOST_DIR=$(shell pwd) \
		-e HOST_HOME=${HOME} \
		-e SSH_AUTH_SOCK="${SSH_AUTH_SOCK}" \
		-volume="${SSH_AUTH_SOCK}:${SSH_AUTH_SOCK}" \
		--rm \
		-idt \
		--volume="${HOME}:${HOME}:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		tsar \
		python "$(shell pwd)/tsar/app/app.py"

shell: build 
	docker run \
		-p 8137:8137 \
		--name tsar \
		-e HOST_USER=${USER} \
		-e HOST_DIR=$(shell pwd) \
		-e HOST_HOME=${HOME} \
		--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock \
		-e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock" \
		--rm \
		-it \
		--volume="${HOME}:${HOME}:cached" \
		--volume="${HOME}/.ipython:/root/.ipython:cached" \
		--memory="2g" \
		--detach-keys="ctrl-q" \
		tsar \
		bash

else
# TARGETS WHEN OS IS UNDETERMINED

shell: 
	echo "unable to determine system in Makefile"
run: 
	echo "unable to determine system in Makefile"
endif
