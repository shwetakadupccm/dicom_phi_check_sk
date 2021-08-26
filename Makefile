.PHONY: style types test quality init check

PY_VER=python3.8
PY_VER_SHORT=py$(shell echo $(PY_VER) | sed 's/[^0-9]*//g')
VENV=env
CODE_DIRS=dicom_phi_check tests
LINE_LEN=120
PYTHON=$(VENV)/bin/python3

style: $(VENV)
	$(PYTHON) -m autoflake -r -i --remove-all-unused-imports --remove-unused-variables $(CODE_DIRS)
	$(PYTHON) -m isort $(CODE_DIRS) --line-length $(LINE_LEN) 
	$(PYTHON) -m autopep8 -a -r -i --max-line-length=$(LINE_LEN) $(CODE_DIRS) 
	$(PYTHON) -m black --line-length $(LINE_LEN) --target-version $(PY_VER_SHORT) $(CODE_DIRS)

types: node_modules
	npx --no-install pyright $(CODE_DIRS) -p pyrightconfig.json

test: $(VENV)
	$(PYTHON) -m pytest tests

quality: $(VENV)
	$(PYTHON) black --check *.py --line-length=120
	$(PYTHON) flake8 *.py

$(VENV):
	$(MAKE) init

init:
	python3 -m virtualenv -p $(PY_VER) $(VENV)
	$(VENV)/bin/pip install -e .[dev]

node_modules:
	npm install

check:
	$(MAKE) style
	$(MAKE) types
	$(MAKE) test

circleci:
	circleci local execute --job run_check
