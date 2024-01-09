# Build configuration
# -------------------

APP_NAME = "task-tracker"
GIT_REVISION = `git rev-parse HEAD`
PSQL_CONTAINER_NAME = task-tracker-postgresql 
CONTAINER_NAME = task-tracker-backend
DATABASE_NAME = task-tracker-postgresql
FIXTURE_FILE = "task_fixture.json"

# Introspection targets
# ---------------------

.PHONY: help
help: header targets

.PHONY: header
header:
	@echo "\033[34mEnvironment\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@printf "\033[33m%-23s\033[0m" "APP_NAME"
	@printf "\033[35m%s\033[0m" $(APP_NAME)
	@echo ""
	@printf "\033[33m%-23s\033[0m" "GIT_REVISION"
	@printf "\033[35m%s\033[0m" $(GIT_REVISION)
	@echo "\n"

.PHONY: targets
targets:
	@echo "\033[34mDevelopment Targets\033[0m"
	@echo "\033[34m---------------------------------------------------------------\033[0m"
	@perl -nle'print $& if m{^[a-zA-Z_-]+:.*?## .*$$}' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-22s\033[0m %s\n", $$1, $$2}'

# Development targets
# -------------

.PHONY: run
run: start

.PHONY: clean ## Delete all temporary files
clean:
	rm -rf .ipynb_checkpoints
	rm -rf **/.ipynb_checkpoints
	rm -rf .pytest_cache
	rm -rf **/.pytest_cache
	rm -rf __pycache__
	rm -rf **/__pycache__
	rm -rf build
	rm -rf dist

.PHONY: build
build: ## build the server
	docker compose build

.PHONY: down 
down: ## Starts the server
	docker compose down

.PHONY: start
start: ## Starts the server
	docker compose up

.PHONY: shell
shell: ## container shell
	docker exec -it $(CONTAINER_NAME) sh -c "clear; (bash || ash || sh)"

.PHONY: attach
attach: ## attach container 
	docker attach $(CONTAINER_NAME)

.PHONY: migrate
migrate: ## Run the migrations
	docker exec -it $(CONTAINER_NAME) python manage.py migrate

.PHONY: loaddata 
loaddata: ## Load fixture data
	docker exec -it $(CONTAINER_NAME) python manage.py loaddata ${FIXTURE_FILE}

.PHONY: migrations
migrations: ## Create migrations
	docker exec -it $(CONTAINER_NAME) python manage.py makemigrations 


.PHONY: tests
tests: ## Run test
	docker exec -it $(CONTAINER_NAME) python manage.py test $(args)

.PHONY: psql
psql: ## Connect to the database
	docker exec -it $(PSQL_CONTAINER_NAME) psql -U postgres -d $(DATABASE_NAME)


# Check, lint and format targets
# ------------------------------

.PHONY: check
check: check-format lint

.PHONY: check-format
check-format: ## Dry-run code formatter
	docker exec -it $(CONTAINER_NAME) black ./ --check
	docker exec -it $(CONTAINER_NAME) isort ./ --profile black --check

.PHONY: lint
lint: ## Run linter
	docker exec -it $(CONTAINER_NAME) pylint ./api ./app ./core
 
.PHONY: format
format: ## Run code formatter
	docker exec -it $(CONTAINER_NAME) black ./
	docker exec -it $(CONTAINER_NAME) isort ./ --profile black
