#!/bin/sh

sleep 1
python manage.py migrate --no-input
exec "$@"
