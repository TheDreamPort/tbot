#!/bin/bash

echo "run database migrations"
(
    flock -e 201

    python3 manage.py migrate           # Apply database migrations


    python3 manage.py collectstatic --noinput  # Collect static files

) 201>/usr/src/app/api-migrations.lock

#./manage.py runserver 0.0.0.0:8080
exec python3 manage.py runworker -v2 channels
