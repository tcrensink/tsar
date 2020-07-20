# network=host allows host/container to share network
# use `host.docker.internal` to connect from container -> host on mac
# rm: clean up docker image on exit
# -it creates interactive (pseudo) tty shell
# see also: reattach_shell.sh in ./resources

build:
	docker build \
		--network=host \
		-t tsar . \
		--build-arg tsar_folder=$(shell pwd)

# rebuild, run app in container
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
		--detach-keys="ctrl-v" \
		tsar \
		bash
