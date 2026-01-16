FROM php:8.3-apache

# Enable Apache rewrite module so .htaccess routing works
RUN a2enmod rewrite \
  && sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

WORKDIR /var/www/html

# Copy public files (index.php + .htaccess)
COPY public/ /var/www/html/

# Document the container port (host port is configured in docker-compose)
EXPOSE 80
