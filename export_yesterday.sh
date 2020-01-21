#!/bin/bash
export HA4SJB_HOME=/datas/vol2/w4a149500/home/w4a149500/ha4sjb
cd "${HA4SJB_HOME}"
source .env
source "${PYTHON_VENV_DIR}"/activate
YESTERDAY="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python exporter.py "${YESTERDAY}"