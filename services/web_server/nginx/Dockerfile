FROM nginx:1.17

COPY ./secrets/nginx/server_certificate.pem /etc/nginx/ssl/server_certificate.pem
COPY ./secrets/nginx/server_key.pem /etc/nginx/ssl/server_key.pem
COPY ./secrets/nginx/ca_certificate.pem /etc/nginx/ssl/ca_certificate.pem
COPY ./secrets/nginx/dhparams.pem /etc/nginx/ssl/dhparams.pem

RUN chown -R www-data:www-data /etc/nginx/ssl

RUN touch /var/run/nginx.pid && \
  chown -R www-data:www-data /var/run/nginx.pid && \
  chown -R www-data:www-data /var/cache/nginx

USER www-data
