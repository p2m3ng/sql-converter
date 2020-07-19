install:
	pip install -r requirements.txt
	pip install -e .

## Clean repository

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
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
up:
	docker-compose up -d

db:
	docker exec -i sqlco-mysql mysql -uroot -ppassword < dev/mysqlsampledatabase.sql

conn:
	docker exec -ti sqlco-mysql mysql -uroot -ppassword

down:
	docker-compose down --remove-orphans

## Tests

test:
	py.test

coverage:
	py.test --cov=.
	coverage html
	sensible-browser htmlcov/index.html

zz:
	GRANT ALL TO 'user'@'localhost' IDENTIFIED BY 'user' ; FLUSH PRIVILEGES;