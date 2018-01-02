# Setup the virtual environment
PYTHON="venv/bin/python"
PIP="venv/bin/pip"
PYTEST="venv/bin/py.test"
TIMESWITCH="venv/bin/timeswitch"

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	$(PIP) install -Ur requirements.txt
	touch venv/bin/activate

venv: venv/bin/activate

# Setup initial database
DATABASE_FILENAME="schedule.sqlite"

$(DATABASE_FILENAME): venv
	$(TIMESWITCH) --create --file $(DATABASE_FILENAME)

# Setup developer environment

install_editable:
	$(PIP) install -e .

install_dev: | install_editable $(DATABASE_FILENAME)

# Run commands

run_dev: install_dev $(DATABASE_FILENAME)
	$(TIMESWITCH) --file $(DATABASE_FILENAME)

run_dev_static: install_dev $(DATABASE_FILENAME)
	$(TIMESWITCH) --file $(DATABASE_FILENAME) --static 'static'

# Build lrelease package

dist: venv
	$(PYTHON) setup.py sdist --formats=zip
	unzip dist/*.zip -d dist/

# Run tests

test:
	$(PYTEST) --ignore=docs/ --cov=timeswitch --cov-report term-missing --tb=line

.PHONY : install_dev install_editable run_dev dist test
