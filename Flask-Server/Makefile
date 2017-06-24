# Setup the virtual environment
PYTHON="venv/bin/python"
PIP="venv/bin/pip"

venv/bin/activate: requirements.txt
	test -d venv || virtualenv -p python3 venv
	$(PIP) install -Ur requirements.txt
	touch venv/bin/activate

venv: venv/bin/activate

# Setup initial database
DATABASE_FILENAME="schedule.sqlite"

$(DATABASE_FILENAME): venv
	timeswitch --create --file $(DATABASE_FILENAME)

# Setup developer environment

install_editable:
	$(PIP) install -e .

install_dev: | install_editable $(DATABASE_FILENAME)

run_dev: install_dev $(DATABASE_FILENAME)
	timeswitch --file $(DATABASE_FILENAME)

dist: venv
	$(PYTHON) setup.py sdist

.PHONY : install_dev install_editable run_dev dist
