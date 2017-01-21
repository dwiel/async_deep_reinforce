.PHONY: build run

build:
	@docker build -t async_deep_reinforce .

run: build
	@docker run --rm -it async_deep_reinforce

shell: build
	@docker run --rm -it async_deep_reinforce /bin/bash

test: build
	@docker run --rm -t async_deep_reinforce_test .
