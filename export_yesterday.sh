#!/bin/bash
source .env
cd "${HA4SJB_HOME}"
source "${PYTHON_VENV_DIR}"/activate
YESTERDAY="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python exporter.py "${YESTERDAY}"