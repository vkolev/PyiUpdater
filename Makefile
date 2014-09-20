binary:
	python dev/make_binary.py

deps:
	pip install -r requirements.txt

deps-upgrade:
	pip install -r requirements.txt --upgrade

deps-dev: deps
	pip install -r requirements.txt
	pip install -r dev/requirements.txt

deps-dev-upgrade: deps-upgrade
	pip install -r requirements.txt --upgrade
	pip install -r dev/requirements.txt --upgrade

pypi:
	python setup.py sdist upload -r pypi

pypi-test:
	python setup.py sdist upload -r pypitest

register:
	python setup.py register -r pypi

register-test:
	python setup.py register -r pypitest

test:
	nosetests -v

test-cover:
	nosetests -v --with-coverage --cover-package=pyi_updater

test-cover-all:
	nosetests -v --with-coverage --cover-package=pyi_updater --cover-package=cli --cover-html

upload:
	twine upload dist/*
