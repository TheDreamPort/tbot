#!/bin/bash

NGINX_CONF=/etc/nginx/conf.d/tbot.conf
CN_NAME=tbot.misi.tech

# If we don't have certs from a volume map, then let's gen them
if [ ! -f /etc/ssl/certs/nginx.crt ]; then
    echo "NGINX certs not found, creating self signed..."
    mkdir -p /etc/ssl/certs
    mkdir -p /etc/ssl/private
    cd /tmp
    openssl req -new -newkey rsa:2048 -days 1825 -nodes -x509 -keyout nginx.key -subj /CN=${CN_NAME} -out nginx.crt
    mv /tmp/nginx.key /etc/ssl/private/nginx.key
    mv /tmp/nginx.crt /etc/ssl/certs/nginx.crt
fi

chmod og-rwx /etc/ssl/private/nginx.key
echo "Starting nginx..."
exec nginx -g "daemon off;"
