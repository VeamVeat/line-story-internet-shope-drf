#!/bin/sh

sleep 1
python manage.py flush --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear
exec "$@"
