#!/bin/bash
source NotionCalendar/bin/activate
echo ".................................... $(date)" >> log.txt
python3 ./main.py >> log.txt

