#!/bin/bash

if [ -n "$REDIS_HOST" ]; then
    # Wait for Redis to come up
    # From https://github.com/dominionenterprises/tol-api-php/blob/master/tests/provisioning/set-env.sh
    while ! exec 6<>/dev/tcp/${REDIS_HOST}/6379; do
        # See http://tldp.org/LDP/abs/html/devref1.html for description of this syntax.
        echo "$(date) - Waiting for REDIS to come up at $REDIS_HOST:6379..."
        sleep 1
    done
    sleep 2 # Wait 2 more seconds to make sure Redis is ready for connections after starting to listen on port
fi

echo "run database migrations"
(
    flock -e 201

    python3 manage.py migrate           # Apply database migrations


    python3 manage.py collectstatic --noinput  # Collect static files

) 201>/usr/src/app/api-migrations.lock


# Start Daphne processes
echo Starting Daphne.
exec daphne -b 0.0.0.0 -p 8000 rest_api.asgi:application