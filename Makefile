SHELL := /bin/bash

H4SJB=.

help:			## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

run:
	@echo -e "\033[35m > Run h4sjb  \033[0m"
	source .env
	python exporter.py

build:
	@echo -e "\033[35m > Run h4sjb  \033[0m"
	source .env
	pip install -r requirements.txt
