#!/bin/bash
source .env
OUTPUT="$(date -d 'yesterday 13:00' '+%Y-%m-%d')"
python exporter.py "${OUTPUT}"