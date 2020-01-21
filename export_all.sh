#!/bin/bash
source .env
cd "${HA4SJB_HOME}"
source "${PYTHON_VENV_DIR}"/activate
python exporter.py 2019-07-01