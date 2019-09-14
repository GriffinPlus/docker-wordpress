# Docker Image with the latest WordPress version on top of NGINX and PHP7.2-FPM

[![Build Status](https://dev.azure.com/griffinplus/Docker%20Images/_apis/build/status/10?branchName=master)](https://dev.azure.com/griffinplus/Docker%20Images/_build/latest?definitionId=10&branchName=master)
[![Docker Pulls](https://img.shields.io/docker/pulls/griffinplus/wordpress.svg)](https://hub.docker.com/r/griffinplus/wordpress)
[![Github Stars](https://img.shields.io/github/stars/griffinplus/docker-wordpress.svg?label=github%20%E2%98%85)](https://github.com/griffinplus/docker-wordpress)
[![Github Stars](https://img.shields.io/github/contributors/griffinplus/docker-wordpress.svg)](https://github.com/griffinplus/docker-wordpress)
[![Github Forks](https://img.shields.io/github/forks/griffinplus/docker-wordpress.svg?label=github%20forks)](https://github.com/griffinplus/docker-wordpress)

## Overview
This Docker image derives from the [nginx-php7.2](https://github.com/griffinplus/docker-nginx-php7.2) image and installs
the latest version of [Wordpress](https://github.com/wordpress/wordpress) that is available on GitHub.

## For Users

### The Initial Startup

The container keeps the entire WordPress installation at `/var/www/html`. Initially there is no configuration file
`wp-config.php` that contains the settings for the database and security keys. The startup script sets everything
up for you, so you don't have to use the WordPress setup wizzard. The startup script copies the sample configuration
file `wp-config-sample.php` shipped with the WordPress installation to `wp-config.php` and applies the desired settings
specified using environment variables below. At least `WORDPRESS_DB_HOST`, `WORDPRESS_DB_USER`, `WORDPRESS_DB_PASSWORD`
are required when running the container the first time.

If you want to persist your WordPress installation, installed addons and uploaded content across container restarts,
you should create a named volume and mount it at `/var/www/html` in the container. Otherwise Docker will delete the
container at shutdown including all the addons and additional content!

### Environment Variables

#### STARTUP_VERBOSITY

Determines the verbosity of the *Griffin+ Container Startup System* (see [here](https://github.com/GriffinPlus/docker-base/tree/master/base)
for details).

- 0 => Logging is disabled.
- 1 => Only errors are logged.
- 2 => Errors and warnings are logged.
- 3 => Errors, warnings and notes are logged.
- 4 => Errors, warnings, notes and infos are logged.
- 5 => All messages (incl. debug) are logged.

Default Value: `4`

#### WORDPRESS_DB_HOST

The name of the host running the MySQL/MariaDB database WordPress will use.

This setting is mandatory, if WordPress does not have a `wp-config.php` file, yet.

The setting in `wp-config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_USER

The name of the database user to use to log in to the database.

This setting is mandatory, if WordPress does not have a `wp-config.php` file, yet.

The setting in `wp-config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_PASSWORD

The password of the database user to use to log in to the database.

This setting is mandatory, if WordPress does not have a `wp-config.php` file, yet.

The setting in `wp-config.php` is overridden, if this environment variable is specified.

#### WORDPRESS_DB_NAME

The name of the database to use.

The setting in `wp-config.php` is overridden, if this environment variable is specified.

Default Value: `wordpress`

#### WORDPRESS_TABLE_PREFIX

The database table prefix to use.

The setting in `wp-config.php` is overridden, if this environment variable is specified.

Default Value: `wp_`

#### WordPress Security Keys

The following environment variables force security keys (`AUTH_KEY`, `AUTH_SALT`, `SECURE_AUTH_KEY`, `SECURE_AUTH_SALT`,
`LOGGED_IN_KEY`, `LOGGED_IN_SALT`, `NONCE_KEY` and `NONCE_SALT`) to be set in `wp-config.php`. A random character
sequence is generated, if `wp-config.php` is created initially. The setting in `wp-config.php` is not touched, if
`wp-config.php` already exists and the corresponding environment variables are not specified.

- WORDPRESS_AUTH_KEY
- WORDPRESS_AUTH_SALT
- WORDPRESS_SECURE_AUTH_KEY
- WORDPRESS_SECURE_AUTH_SALT
- WORDPRESS_LOGGED_IN_KEY
- WORDPRESS_LOGGED_IN_SALT
- WORDPRESS_NONCE_KEY
- WORDPRESS_NONCE_SALT

#### PHP Specific Settings

Please see the documentation of the [nginx-php7.2](https://github.com/griffinplus/docker-nginx-php7.2) image for
available configuration options concerning PHP7.2-FPM.
