include .env

FILE=tests/
FUNC=""

.PHONY: test
test:
	docker-compose exec ${CONTAINER_NAME} pytest -s ${FILE} -k ${FUNC}
