#!/bin/bash
source /home/fhzdcizd/virtualenv/backend/3.6/bin/activate && cd /home/fhzdcizd/backend
python manage.py emp_cron
deactivate
