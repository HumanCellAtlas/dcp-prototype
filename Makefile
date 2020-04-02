SHELL:=/bin/bash

.PHONY: fmt
fmt:
	black .
	terraform fmt -recursive infra

.PHONY: lint
lint:
	flake8 dcp_prototype tests

.PHONY: unit-test
unit-test:
	PYTHONWARNINGS=ignore:ResourceWarning coverage run \
		--source=dcp_prototype/backend, \
		--omit=.coverage,venv,dcp_prototype/backend/browser/scripts,dcp_prototype/backend/browser/api \
		-m unittest discover \
		--start-directory tests/unit \
		--top-level-directory . \
		--verbose

.PHONY: functional-test
functional-test:
	$(MAKE) package -C dcp_prototype/backend/browser/api
	python3 -m unittest discover --start-directory tests/functional --top-level-directory . --verbose
