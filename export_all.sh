#!/bin/bash
cd "${HA4SJB_HOME}"
source "${HA4SJB_HOME}"/.env
source "${HA4SJB_HOME}"/"${PYTHON_VENV_DIR}"/activate
python "${HA4SJB_HOME}"/exporter.py 2019-07-01