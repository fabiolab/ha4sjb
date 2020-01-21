#!/bin/bash
cd "${HA4SJB_HOME}"
source .env
source "${PYTHON_VENV_DIR}"/activate
YESTERDAY="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python exporter.py "${YESTERDAY}"