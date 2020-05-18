FROM nginx:stable-alpine

RUN apk add openssl ca-certificates && mkdir /etc/nginx/conf.d/available /etc/nginx/conf.d/enabled

# Add the nginx configs, and run script
ADD nginx_example.conf /etc/nginx/nginx.conf
ADD run.sh /

# Remove existing files, and copy over the react app
RUN rm -rf /var/www/html

# Ensure our run script is executable and get rid of the default config
RUN chmod +x /run.sh && \
    rm /etc/nginx/conf.d/default.conf

CMD ["/bin/sh", "/run.sh"]
