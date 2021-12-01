all: lint

lint:
	python3 -m mypy gdrive_lib/**/*.py
	python3 -m mypy examples/*.py
	python3 -m pylint gdrive_lib/**/*.py
	python3 -m pylint examples/*.py

install-deps:
	pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client mypy pylint
