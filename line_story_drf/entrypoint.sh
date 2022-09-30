#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done
    echo "PostgresSQL started"
fi

python manage.py flush --no-input
python manage.py migarate

exec "$@"

#python manage.py makemigrations --noinput
#python manage.py migrate --noinput
#gunicorn line_story_drf.wsgi:application --bind 0.0.0.0:8000