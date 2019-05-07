TRAVIS_YML=.travis.yml
TOX2TRAVIS=tox2travis.py
.PHONY: clean-python clean-build docs clean-tox ${TRAVIS_YML} ci no-readme-errors
PYPI_SERVER?=pypi
GIT_REMOTE_NAME?=origin
SHELL=/bin/bash
VERSION=$(shell python -c"import djactasauth as m; print(m.__version__)")

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-python - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "testall - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation"
	@echo "tag - tag the current version and push it to origin"
	@echo "release - package and upload a release"
	@echo "sdist - package"
	@echo "${TRAVIS_YML} - convert tox.ini to ${TRAVIS_YML}"

ci: ${TRAVIS_YML} test-all

${TRAVIS_YML}: DIFF_CMD=diff ${TRAVIS_YML} ${OUTFILE}
${TRAVIS_YML}: OUTFILE=${TRAVIS_YML}.generated
${TRAVIS_YML}: tox.ini ${TOX2TRAVIS}
	./${TOX2TRAVIS} > ${OUTFILE}
	${DIFF_CMD}; echo $$?  # FYI
	test 0 -eq $$(${DIFF_CMD} | wc -l)

clean: clean-build clean-python clean-tox

clean-build:
	rm -fr build/
	rm -fr dist/
	find -name *.egg-info -type d | xargs rm -rf

clean-python:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -type d -exec rm -rf {} +

clean-tox:
	if [[ -d .tox ]]; then rm -r .tox; fi

lint:
	flake8 tests --isolated
	flake8 djactasauth --isolated --max-complexity=6

test:
	python manage.py test testapp --traceback

test-all:
	tox

coverage:
	coverage run --source djactasauth setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	make -C docs html

no-readme-errors:
	rst2html.py README.rst > /dev/null 2> $@
	cat $@
	test 0 -eq `cat $@ | wc -l`

release: TAG:=v${VERSION}
release: exit_code:=$(shell git ls-remote origin | grep -q tags/${TAG}; echo $$?)
release:
ifeq ($(exit_code),0)
	@echo "Tag ${TAG} already present"
else
	git tag -a ${TAG} -m"${TAG}"; git push --tags origin
endif
