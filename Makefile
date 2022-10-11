include .env
include makefiles/formatter.mk
include makefiles/m1_mac.mk
include makefiles/pytest.mk
include makefiles/utils.mk

.PHONY: build_pkg
build_pkg:
	poetry build


.PHONY: up
up:
	docker-compose up


.PHONY: build
build:
	docker-compose build


.PHONY: bash
bash:
	docker-compose exec ${CONTAINER_NAME} /bin/bash


.PHONY: clear
clear:
	docker-compose down --rmi all --volumes
