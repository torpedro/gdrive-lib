
lint:
	python3 -m mypy src/**/*.py
	python3 -m pylint src/**/*.py

setup-venv:
	python3 -m venv .google-drive-venv
	
install-deps:
	pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client mypy pylint
