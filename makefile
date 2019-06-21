
.PHONY: clean
clean:
	rm -rf dist/*
	mkdir -p dist/

.PHONY: build
build: clean
	pipenv lock -r 1> dist/requirements.txt	
	# fancy copy (minus tests, minus pyc files)
	rsync -av src/* dist --exclude tests --exclude __pycache__ --exclude *.pyc
	
.PHONY: doc_test
doc_test:
	pipenv run python -m doctest src/logger.py

.PHONY: test
test: 
	pipenv run python -m pytest -W ignore::DeprecationWarning src

.PHONY: all_test
all_test: doc_tests test

.PHONY: setup
setup:
	echo "This should only need to be run once, during your initial project setup on your computer"
	echo "Also, this should not be run as root"
	pip install --user pipenv
	pipenv install

.PHONY: local_docker
local_docker: build
	sudo docker build -t risklens-logreader-be-dev -f Dockerfile.dev .

.PHONY: run
run: build
	sudo docker-compose build
	sudo docker-compose up