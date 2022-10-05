#!/bin/sh

sleep 1
python manage.py flush --no-input
python manage.py migrate --no-input
exec "$@"
