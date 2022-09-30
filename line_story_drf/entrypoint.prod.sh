#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $DB_HOST $DB_POST; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi
exec "$@"



#python manage.py makemigrations --noinput
#python manage.py migrate --noinput
#gunicorn line_story_drf.wsgi:application --bind 0.0.0.0:8000