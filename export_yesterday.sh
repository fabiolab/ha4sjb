#!/bin/bash
cd "${HA4SJB_HOME}"
source "${HA4SJB_HOME}"/.env
source "${HA4SJB_HOME}"/"${PYTHON_VENV_DIR}"/activate
YESTERDAY="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python "${HA4SJB_HOME}"/exporter.py "${YESTERDAY}"