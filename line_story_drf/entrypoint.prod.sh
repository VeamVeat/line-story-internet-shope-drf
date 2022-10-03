#!/bin/sh

sleep 1
python manage.py collectstatic --noinput
python manage.py migrate
exec "$@"
