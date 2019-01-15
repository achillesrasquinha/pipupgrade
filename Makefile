.PHONY: shell test help

BASEDIR					= $(shell pwd)
-include ${BASEDIR}/.env

ENVIRONMENT			   ?= development

PROJECT					= pipupgrade

PROJDIR					= ${BASEDIR}/src/pipupgrade
TESTDIR					= ${BASEDIR}/tests

PYTHONPATH		 	   ?= python

VIRTUAL_ENV			   ?= ${BASEDIR}/.venv
VENVBIN					= ${VIRTUAL_ENV}/bin

PYTHON				  	= ${VENVBIN}/python
IPYTHON					= ${VENVBIN}/ipython
PIP					  	= ${VENVBIN}/pip
PYTEST					= ${VENVBIN}/pytest
TOX						= ${VENVBIN}/tox
COVERALLS				= ${VENVBIN}/coveralls
TWINE					= ${VENVBIN}/twine
IPYTHON					= ${VENVBIN}/ipython
BUMPVERSION				= ${VENVBIN}/bumpversion
SAFETY					= ${VENVBIN}/safety

JOBS				   ?= $(shell $(PYTHON) -c "import multiprocessing as mp; print(mp.cpu_count())")
PYTHON_ENVIRONMENT      = $(shell $(PYTHON) -c "import sys;v=sys.version_info;print('py%s%s'%(v.major,v.minor))")

NULL					= /dev/null

define log
	$(eval CLEAR     = \033[0m)
	$(eval BOLD		 = \033[0;1m)
	$(eval INFO	     = \033[0;36m)
	$(eval SUCCESS   = \033[0;32m)

	$(eval BULLET 	 = "→")
	$(eval TIMESTAMP = $(shell date +%H:%M:%S))

	@echo "${BULLET} ${$1}[${TIMESTAMP}]${CLEAR} ${BOLD}$2${CLEAR}"
endef

define browse
	$(PYTHON) -c "import webbrowser as wb; wb.open('${$1}')"
endef

ifndef VERBOSE
.SILENT:
endif

.DEFAULT_GOAL 		   := help 

env: ## Create a Virtual Environment
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif

	$(call log,INFO,Creating a Virtual Environment ${VIRTUAL_ENV} with Python - ${PYTHONPATH})
	@virtualenv $(VIRTUAL_ENV) -p $(PYTHONPATH) $(OUT)

info: ## Display Information
	@echo "Python Environment: ${PYTHON_ENVIRONMENT}"

install: clean info ## Install dependencies and module.
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif

ifneq (${PIPCACHEDIR},)
	$(eval PIPCACHEDIR = --cache-dir $(PIPCACHEDIR))
endif

	$(call log,INFO,Building Requirements)
	@find $(BASEDIR)/requirements -maxdepth 1 -type f | xargs awk '{print}' > $(BASEDIR)/requirements-dev.txt
	@cat $(BASEDIR)/requirements/production.txt  > $(BASEDIR)/requirements.txt

	$(call log,INFO,Installing Requirements)
	$(PIP) install -r $(BASEDIR)/requirements-dev.txt $(OUT)

	$(call log,INFO,Installing ${PROJECT} (${ENVIRONMENT}))
ifeq (${ENVIRONMENT},production)
	$(PYTHON) setup.py install $(OUT)
else
	$(PYTHON) setup.py develop $(OUT)
endif

	$(call log,SUCCESS,Installation Successful)

clean: ## Clean cache, build and other auto-generated files.
ifneq (${ENVIRONMENT},test)
	@clear

	$(call log,INFO,Cleaning Python Cache)
	@find $(BASEDIR) | grep -E "__pycache__|\.pyc" | xargs rm -rf

	@rm -rf \
		$(BASEDIR)/*.egg-info \
		$(BASEDIR)/.pytest_cache \
		$(BASEDIR)/.tox \
		$(BASEDIR)/*.coverage \
		$(BASEDIR)/*.coverage.* \
		$(BASEDIR)/htmlcov \
		$(BASEDIR)/dist \
		$(BASEDIR)/build \

	$(call log,SUCCESS,Cleaning Successful)
else
	$(call log,SUCCESS,Nothing to clean)
endif

test: install ## Run tests.
	$(call log,INFO,Running Python Tests using $(JOBS) jobs.)
	$(TOX) --skip-missing-interpreters $(ARGS)

coverage: install ## Run tests and display coverage.
ifeq (${ENVIRONMENT},development)
	$(eval IARGS := --cov-report html)
endif

	$(PYTEST) -n $(JOBS) --cov $(PROJDIR) $(IARGS) -vv $(ARGS)

ifeq (${ENVIRONMENT},development)
	$(call browse,file:///${BASEDIR}/htmlcov/index.html)
endif

ifeq (${ENVIRONMENT},test)
	$(COVERALLS)
endif

bump: ## Bump Version
	echo $(VERSION) > $(PROJDIR)/VERSION

	git add $(PROJDIR)/VERSION
	git commit -m "Bumped to Version $(VERSION)"

release: test build ## Create a Release (DEPRECATED - Use auto-deploy using .travis.yml)
ifeq (${ENVIRONMENT},development)
	$(call log,WARN,Ensure your environment is in production mode.)
	$(TWINE) upload --repository-url https://test.pypi.org/legacy/   $(BASEDIR)/dist/* 
else
	$(TWINE) upload --repository-url https://upload.pypi.org/legacy/ $(BASEDIR)/dist/* 
endif

shell: ## Launch an IPython shell.
	$(call log,INFO,Launching Python Shell)
	$(IPYTHON) \
		--no-banner

build:  clean ## Build the Distribution.
	$(PYTHON) setup.py sdist bdist_wheel

docker-build: clean ## Build the Docker Image.
	$(call log,INFO,Building Docker Image)
ifeq (${TRAVIS_BRANCH},master)
	$(eval BRANCH = latest)
endif

	@docker build $(BASEDIR) --tag $(DOCKER_HUB_USERNAME)/$(PROJECT):$(BRANCH)

docker-tox: clean ## Test using Docker Tox Image.
	$(call log,INFO,Testing the Docker Image)
	@docker run --rm -v $(shell pwd):/app themattrix/tox

help: ## Show help and exit.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)