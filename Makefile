.EXPORT_ALL_VARIABLES:

AWS_REGION ?= ap-southeast-2
SRC_PATH := ingenico_mantalus_support_sns_topic

ifdef STACK_NAME
	STACKS := $(STACK_NAME)
else
	STACKS := --all
endif

define HELP

This is the ingenico-mantalus-support-sns-topic Makefile.

Usage:

make [deploy|synth|diff|list-stacks] ENVIRONMENT=[mantalus-dev,mantalus-prod,etc]
make [test|black|ruff|lint|yamllint]

make deploy|synth|diff - Runs cdk commands as target
make test - Runs pytest
make black|ruff|lint|yamllint - Runs linting, formatting, etc

endef

export HELP

help:
	@echo "$$HELP"

.PHONY: run deploy diff synth test format ruff check

all: test deploy

install:
	python -m pip install -r ./requirements.txt;

deploy diff synth: envvars
	npx cdk $@ $(STACKS) --require-approval never $(DEBUG)

destroy: envvars
	npx cdk $@ $(STACKS) --require-approval never $(DEBUG)

list-stacks: envvars
	npx cdk ls --all --require-approval never $(DEBUG)

test:
	pytest tests/ -v

typecheck:
	mypy .

black:
	black --check $(SRC_PATH)

format:
	black $(SRC_PATH) app.py

ruff:
	ruff check .

yamllint:
	yamllint config/ .github/workflows

lint: black ruff typecheck yamllint

check: lint test

envvars:
ifndef INGENICO_MMS_TOPIC_ENVIRONMENT
	$(error INGENICO_MMS_TOPIC_ENVIRONMENT is not set)
endif