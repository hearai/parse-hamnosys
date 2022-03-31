################################################################
# GLOBALS													   #
################################################################

PROJECT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME := hearai
PYTHON ?= python3
VENV = $(PROJECT_DIR)/.venv
PIP = $(VENV)/bin/pip
VIRTUALENV = $(PYTHON) -m venv
SHELL=/bin/bash

################################################################
# VIRTUAL ENVIRONMENT AND DEPENDENCIES						   #
################################################################

.PHONY: venv
## create virtual environment
venv: ./.venv/.requirements
        
.venv:
		$(VIRTUALENV) $(VENV)
		$(PIP) install -U pip setuptools wheel

.venv/.requirements: .venv
		$(PIP) install -r $(PROJECT_DIR)/requirements.txt -r $(PROJECT_DIR)/requirements-dev.txt
		touch $(VENV)/.requirements

.PHONY: venv-clean
## clean virtual environment
venv-clean: