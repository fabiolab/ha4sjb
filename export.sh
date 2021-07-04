#!/bin/bash
export HA4SJB_HOME=/home/kvjw3322/Developement/perso/ha4sjb
export PYTHON_VENV_DIR=/home/kvjw3322/Developement/perso/ha4sjb/p3.8/bin
cd "${HA4SJB_HOME}"
source .env
source "${PYTHON_VENV_DIR}"/activate
pip install -r requirements.txt
python exporter.py