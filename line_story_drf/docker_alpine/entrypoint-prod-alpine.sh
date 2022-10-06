#!/bin/sh

sleep 1
python manage.py collectstatic --no-input
python manage.py migrate --no-input
exec "$@"
