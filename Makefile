# rebuild image
build:
	docker build -t tsar .
	# docker build --network=host -t tsar .

# get bash shell in container
shell_only:
	docker run \
		-it \
		--rm \
		--volume="$(shell pwd):/opt" \
		--volume="${HOME}/.ipython:/root/.ipython" \
		tsar \
		bash

shell: build shell_only

run_only:
	docker run \
		-it \
		--rm \
		-v $(shell pwd):/opt \
		tsar

run: build run_only

# (broken example)
# lintfix:
# 	docker run --rm -v $(shell pwd):/code -w /code unibeautify/black -v .
