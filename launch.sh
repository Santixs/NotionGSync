#!/bin/bash
cd scripts/NotionGSync
source NotionCalendar/bin/activate
echo ".................................... $(date)" >> ./log.txt
python3 ./main.py >> ./log.txt

