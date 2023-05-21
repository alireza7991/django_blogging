#!/bin/bash

echo "Waiting for postgres..."
while ! nc -z db 5432; do
    sleep 0.1
done
echo "Postgres started"

echo "Running migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "Migration failed." >&2
    exit 1
fi
echo "Migrations done"

# If we have any args (e.g. running tests), run args,
# otherwise start the server

if [[ $# -gt 0 ]]; then
    INPUT=$@
    sh -c "$INPUT"
else
    echo "Starting application..."
    python manage.py runserver 0.0.0.0:8000
fi