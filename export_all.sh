#!/bin/bash
cd "${HA4SJB_HOME}"
source .env
source "${PYTHON_VENV_DIR}"/activate
python exporter.py 2019-07-01