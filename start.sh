#!/bin/sh

python ./link/manage.py makemigrations
python ./link/manage.py migrate
uwsgi --ini /home/workspace/link/uwsgi.ini
