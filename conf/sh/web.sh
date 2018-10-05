#!/bin/sh
pwd
sleep 5
chown -R 1000 /medicine
su -m appuser -c "python3 manage.py collectstatic --no-input"
su -m appuser -c "python3 manage.py makemigrations user disease"
su -m appuser -c "python3 manage.py migrate user"
su -m appuser -c "python3 manage.py migrate disease"
su -m appuser -c "python3 manage.py migrate"
# chown -r 1000 media/
su -m appuser -c "uwsgi uwsgi.ini"
