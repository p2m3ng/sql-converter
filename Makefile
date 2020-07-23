.PHONY: clean clean-test clean-pyc clean-build help dev install dtest db
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

## Environments

dev: ## install dev environment
	pip install -r requirements/dev.txt
	pip install -e .

install: ## install production environment
	pip install -r requirements/prod.txt
	pip install -e .

## Clean repository

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr builds/
	rm -fr dist/
	rm -fr prof/
	rm -fr .eggs/
	find . -path ./venv -prune -o -name '*.egg-info' -exec rm -fr {} +
	find . -path ./venv -prune -o -name '*.egg' -exec rm -f {} +
	find . -path ./venv -prune -o -name '*.egg' -exec rm -rf {} +

clean-pyc: ## remove Python file artifacts
	find . -path ./venv -prune -o -name '*.pyc' -exec rm -f {} +
	find . -path ./venv -prune -o -name '*.pyo' -exec rm -f {} +
	find . -path ./venv -prune -o -name '*~' -exec rm -f {} +
	find . -path ./venv -prune -o -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

prune-venv:
	rm -fr venv/

## Docker
build:
	docker-compose build

up: ## create containers with sample databases
	docker-compose up -d

db: ## mount sample databases
	mkdir -p db/samples
	wget https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_MySql.sql -O \
	 ./db/samples/chinook.sql
	wget https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite -O \
	./db/samples/chinook.sqlite
# 	docker exec -i sqlco-mysql mysql -uroot -ppassword < db/samples/chinook.sql

conn:
	docker exec -ti sqlco-mysql mysql -uroot -ppassword Chinook

logs:
	docker logs -f sqlco-mysql

down: ## remove containers
	docker-compose down -v --remove-orphans

erase: down ## remove containers and erase volume
	rm-rf volume

## Tests

test-env: db build up ## run test docker and install mysql database

test: ## launch tests
	py.test

coverage: ## check coverage
	py.test --cov=.
	coverage html
