# Docker Image with WordPress 4.x on top of NGINX and PHP7-FPM

[![Build Status](https://travis-ci.org/cloudycube/docker-wordpress.svg?branch=master)](https://travis-ci.org/cloudycube/docker-wordpress) [![Docker 
Pulls](https://img.shields.io/docker/pulls/cloudycube/wordpress.svg)](https://hub.docker.com/r/cloudycube/wordpress) [![Github 
Stars](https://img.shields.io/github/stars/cloudycube/docker-wordpress.svg?label=github%20%E2%98%85)](https://github.com/cloudycube/docker-wordpress) [![Github 
Stars](https://img.shields.io/github/contributors/cloudycube/docker-wordpress.svg)](https://github.com/cloudycube/docker-wordpress) [![Github 
Forks](https://img.shields.io/github/forks/cloudycube/docker-wordpress.svg?label=github%20forks)](https://github.com/cloudycube/docker-wordpress)

## Overview
This Docker image derives from the [nginx-php7](https://github.com/cloudycube/docker-nginx-php7) image and installs the latest version of [Wordpress 4.x](https://github.com/WordPress/WordPress) that is available on GitHub.

This image belongs to a set of Docker images created for project [CloudyCube](http://www.falk-online.eu/projekte/cloudycube). The homepage is in German only, but you will find everything needed to get it working here as well.

## For Users

### Environment Variables

#### WORDPRESS_DB_HOST

The name of the host running the MySQL/MariaDB database WordPress will use.

This setting is mandatory, if WordPress does not have a `wp_config.php` file, yet.

The setting in `wp_config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_USER

The name of the database user to use to log in to the database.

This setting is mandatory, if WordPress does not have a `wp_config.php` file, yet.

The setting in `wp_config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_PASSWORD

The password of the database user to use to log in to the database.

This setting is mandatory, if WordPress does not have a `wp_config.php` file, yet.

The setting in `wp_config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_NAME

The name of the database to use.

The setting in `wp_config.php` is overridden, if this environment variable is specified.

Default Value: `wordpress`

#### WORDPRESS_TABLE_PREFIX

The database table prefix to use.

The setting in `wp_config.php` is overridden, if this environment variable is specified.

Default Value: `wp_`

#### WordPress Security Keys

The following environment variables force security keys (AUTH_KEY, AUTH_SALT, SECURE_AUTH_KEY, SECURE_AUTH_SALT, LOGGED_IN_KEY, LOGGED_IN_SALT, NONCE_KEY and NONCE_SALT) to be set in `wp_config.php`. A random character sequence is generated, if `wp_config.php` is created initially. The setting in `wp_config.php` is not touched, if `wp_config.php` already exists and the corresponding environment variables are not specified.

- WORDPRESS_AUTH_KEY
- WORDPRESS_AUTH_SALT
- WORDPRESS_SECURE_AUTH_KEY
- WORDPRESS_SECURE_AUTH_SALT
- WORDPRESS_LOGGED_IN_KEY
- WORDPRESS_LOGGED_IN_SALT
- WORDPRESS_NONCE_KEY
- WORDPRESS_NONCE_SALT

#### PHP Specific Settings

Please see the documentation of the [nginx-php7](https://github.com/cloudycube/docker-nginx-php7) image for available configuration options.
