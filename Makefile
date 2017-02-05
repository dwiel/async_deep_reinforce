.PHONY: build run

build:
	@docker build -f=Dockerfile -t=async_deep_reinforce .

run: build
	$(eval LOG := $(shell pwd)/log/$(shell date +'%Y%m%d_%H%M%S')_$(shell docker images async_deep_reinforce -q))
	docker run --rm -v ${LOG}:/volume -it async_deep_reinforce

shell: build
	@docker run --rm -it async_deep_reinforce /bin/bash

build_test:
	docker build -f=Dockerfile.test -t=async_deep_reinforce_test .

test: build_test
	@docker run --rm -t async_deep_reinforce_test .
