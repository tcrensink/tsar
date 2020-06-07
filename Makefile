# NOTES FOR OPTIONS IN MAKEFILE:
# share network with host
#
_build:
	docker build --network=host -t tsar .

run:
	docker run \
		-it \
		--rm \
		-v $(shell pwd):/opt \
		tsar \
		bash

build: _build run
