#!/bin/bash
export HA4SJB_HOME=/home/kvjw3322/Nextcloud/Documents/Bad/ha4sjb
cd "${HA4SJB_HOME}"
source .env
source "${PYTHON_VENV_DIR}"/activate
python exporter.py