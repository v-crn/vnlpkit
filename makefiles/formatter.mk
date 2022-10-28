include .env

.PHONY: lint
lint:
	docker-compose exec ${CONTAINER_NAME} pflake8 ${PROJECT_NAME} tests work
	docker-compose exec ${CONTAINER_NAME} mypy ${PROJECT_NAME} tests work


.PHONY: format
format:
	black --exclude=.venv ${PROJECT_NAME} vnlpkit tests work
	autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables ${PROJECT_NAME} vnlpkit tests work
	isort --profile=black ${PROJECT_NAME} vnlpkit tests work

# docker-compose exec ${CONTAINER_NAME} black --exclude=.venv ${PROJECT_NAME} tests work
# docker-compose exec ${CONTAINER_NAME} autoflake -ri --remove-all-unused-imports --ignore-init-module-imports --remove-unused-variables ${PROJECT_NAME} tests work
# docker-compose exec ${CONTAINER_NAME} isort --profile=black ${PROJECT_NAME} tests work
