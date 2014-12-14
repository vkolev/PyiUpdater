binary:
	python dev/make_binary.py

deps:
	pip install -r requirements.txt

deps-upgrade:
	pip install -r requirements.txt --upgrade

deps-dev: deps
	pip install -r dev/requirements.txt

deps-dev-upgrade: deps-upgrade
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
	py.test -v -n 1 --durations=3 -x

test-cover:
	py.test -v --cov src/pyi_updater --cov-report html -n 1

test-script:
	py.test --genscript=runtests.py

upload:
	twine upload dist/*
