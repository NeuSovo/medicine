#!/bin/sh
pwd
sleep 5
python3 manage.py makemigrations user disease
python3 manage.py migrate user
python3 manage.py migrate disease
python3 manage.py migrate
# chown -R 1000 media/
su -m appuser -c "uwsgi uwsgi.ini"
