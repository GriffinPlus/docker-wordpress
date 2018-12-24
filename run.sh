#!/bin/bash

# This script starts a new instance of the griffinplus/wordpress container and opens a shell in it.
# It is useful in cases where some debugging is needed...

DATABASE_HOST='<your database host>'
DATABASE_USER='<your database user>'
DATABASE_PASSWORD='<your database password>'
DATABASE_NAME='<your database name>'

# add a volume that keeps the actual wordpress installation
docker volume create my-wordpress-blog

# run the container
docker run -it \
           --rm \
           --name wordpress \
           --env WORDPRESS_DB_HOST="$DATABASE_HOST" \
           --env WORDPRESS_DB_USER="$DATABASE_NAME" \
           --env WORDPRESS_DB_PASSWORD="$DATABASE_PASSWORD" \
           --env WORDPRESS_DB_NAME="$DATABASE_NAME" \
           --env WORDPRESS_TABLE_PREFIX="wp_" \
           --env CC_STARTUP_VERBOSITY=4 \
           --volume my-wordpress-blog:/var/www/html \
           griffinplus/wordpress \
           run-and-enter

