#!/bin/bash
source .env
cd /datas/vol2/w4a149500/home/w4a149500/ha4sjb
source ./p3.6/bin/activate
YESTERDAY="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python exporter.py "${YESTERDAY}"