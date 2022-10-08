include .env

FILE=tests/
FUNC=""


.PHONY: lint
lint:
	docker-compose exec ${CONTAINER_NAME} pflake8 ${PACKAGE_NAME} tests
	docker-compose exec ${CONTAINER_NAME} mypy ${PACKAGE_NAME} tests


.PHONY: format
format:
	docker-compose exec ${CONTAINER_NAME} black --exclude=.venv ${PACKAGE_NAME} tests
	docker-compose exec ${CONTAINER_NAME} autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables ${PACKAGE_NAME} tests
	docker-compose exec ${CONTAINER_NAME} isort --profile=black ${PACKAGE_NAME} tests


.PHONY: build_pkg
build_pkg:
	poetry build


.PHONY: up
up:
# docker-compose up
	docker-compose -f docker-compose-for-m1-mac.yml up


.PHONY: build
build:
# docker-compose build
	docker-compose -f docker-compose-for-m1-mac.yml build


.PHONY: bash
bash:
	docker-compose exec ${CONTAINER_NAME} /bin/bash


.PHONY: test
test:
	docker-compose exec ${CONTAINER_NAME} pytest -s ${FILE} -k ${FUNC}


.PHONY: clear
clear:
	docker-compose down --rmi all --volumes
