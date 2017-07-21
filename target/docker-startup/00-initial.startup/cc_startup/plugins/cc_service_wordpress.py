"""
This module contains everything needed to configure 'WordPress'.
Author: Sascha Falk <sascha@falk-online.eu>
License: MIT License
"""

import os
import re

from ..cc_helpers import read_text_file, write_text_file, replace_php_define, replace_php_variable, generate_password, get_env_setting_bool, get_env_setting_integer, get_env_setting_string
from ..cc_log import Log
from ..cc_service import Service


CONFIGURATION_FILE_PATH = '/var/www/html/wp-config.php'
SAMPLE_CONFIGURATION_FILE_PATH = '/var/www/html/wp-config-sample.php'


# ---------------------------------------------------------------------------------------------------------------------

# name of the service
service_name = 'WordPress'

# determines whether the service is run by the startup script
enabled = True

def get_service():
    "Returns an instance of the service provided by the service plugin."
    return WordPress()

# ---------------------------------------------------------------------------------------------------------------------


class WordPress(Service):

    def prepare(self):
        """
        Reads environment variables and checks preconditions the following call to configure() needs to succeed. In case
        of anything being screwed in the configuration or system, this method should throw an exception to abort starting
        up before configure() modifies any configuration files.
        """

        # load configuration file (respectively the sample configuration file, if the configuration file does not exist, yet)
        # ---------------------------------------------------------------------------------------
        if os.path.exists(CONFIGURATION_FILE_PATH):
            self._config_file, _ = read_text_file(CONFIGURATION_FILE_PATH, 'utf-8')
            self._config_file_exists = True
        elif os.path.exists(SAMPLE_CONFIGURATION_FILE_PATH):
            self._config_file, _ = read_text_file(SAMPLE_CONFIGURATION_FILE_PATH, 'utf-8')
            self._config_file_exists = False
        else:
           raise RuntimeError('Neither the configuraton file ({0}) nor the sample configuration file ({1}) exists.'.format(CONFIGURATION_FILE_PATH, SAMPLE_CONFIGURATION_FILE_PATH))

        # database
        # ---------------------------------------------------------------------------------------
        self._db_host = get_env_setting_string('WORDPRESS_DB_HOST')
        if not self._db_host and not self._config_file_exists:
            error = 'Environment variable WORDPRESS_DB_HOST is not set.'
            raise RuntimeError(error)

        self._db_user = get_env_setting_string('WORDPRESS_DB_USER')
        if not self._db_user and not self._config_file_exists:
            error = 'Environment variable WORDPRESS_DB_USER is not set.'
            raise RuntimeError(error)

        self._db_password = get_env_setting_string('WORDPRESS_DB_PASSWORD')
        if not self._db_password and not self._config_file_exists:
            error = 'Environment variable WORDPRESS_DB_PASSWORD is not set.'
            raise RuntimeError(error)

        self._db_name = get_env_setting_string('WORDPRESS_DB_NAME')
        self._table_prefix = get_env_setting_string('WORDPRESS_TABLE_PREFIX')

        # cryptographic keys and salts
        # ---------------------------------------------------------------------------------------

        self._auth_key = get_env_setting_string('WORDPRESS_AUTH_KEY')
        self._auth_salt = get_env_setting_string('WORDPRESS_AUTH_SALT')
        self._secure_auth_key = get_env_setting_string('WORDPRESS_SECURE_AUTH_KEY')
        self._secure_auth_salt = get_env_setting_string('WORDPRESS_SECURE_AUTH_SALT')
        self._logged_in_key = get_env_setting_string('WORDPRESS_LOGGED_IN_KEY')
        self._logged_in_salt = get_env_setting_string('WORDPRESS_LOGGED_IN_SALT')
        self._nonce_key = get_env_setting_string('WORDPRESS_NONCE_KEY')
        self._nonce_salt = get_env_setting_string('WORDPRESS_NONCE_SALT')


    # ---------------------------------------------------------------------------------------------------------------------


    def configure(self):
        """
        Creates/modifies the configuration file according to environment variables.
        """

        text = self._config_file

        # ---------------------------------------------------------------------------------------

        if self._config_file_exists:
            # the configuration file exists, i.e. it should already contain valid settings
            # => override settings that have been specified in environment variables
            if self._db_host:          text = replace_php_define(   text, 'DB_HOST',          self._db_host)
            if self._db_user:          text = replace_php_define(   text, 'DB_USER',          self._db_user)
            if self._db_password:      text = replace_php_define(   text, 'DB_PASSWORD',      self._db_password)
            if self._db_name:          text = replace_php_define(   text, 'DB_NAME',          self._db_name)
            if self._auth_key:         text = replace_php_define(   text, 'AUTH_KEY',         self._auth_key)
            if self._auth_salt:        text = replace_php_define(   text, 'AUTH_SALT',        self._auth_salt)
            if self._secure_auth_key:  text = replace_php_define(   text, 'SECURE_AUTH_KEY',  self._secure_auth_key)
            if self._secure_auth_salt: text = replace_php_define(   text, 'SECURE_AUTH_SALT', self._secure_auth_salt)
            if self._logged_in_key:    text = replace_php_define(   text, 'LOGGED_IN_KEY',    self._logged_in_key)
            if self._logged_in_salt:   text = replace_php_define(   text, 'LOGGED_IN_SALT',   self._logged_in_salt)
            if self._nonce_key:        text = replace_php_define(   text, 'NONCE_KEY',        self._nonce_key)
            if self._nonce_salt:       text = replace_php_define(   text, 'NONCE_SALT',       self._nonce_salt)
            if self._table_prefix:     text = replace_php_variable( text, 'table_prefix',     self._table_prefix)
        else:
            # the configuration file does not exist, i.e. the sample file was loaded
            # => override all settings, provide sensible defaults, if necessary)
            text = replace_php_define(   text, 'DB_HOST',          self._db_host)         # always inited, since checked in prepare()
            text = replace_php_define(   text, 'DB_USER',          self._db_user)         # always inited, since checked in prepare()
            text = replace_php_define(   text, 'DB_PASSWORD',      self._db_password)     # always inited, since checked in prepare()
            text = replace_php_define(   text, 'DB_NAME',          self._db_name          if self._db_name          else 'wordpress')
            text = replace_php_define(   text, 'AUTH_KEY',         self._auth_key         if self._auth_key         else generate_password(64))
            text = replace_php_define(   text, 'AUTH_SALT',        self._auth_salt        if self._auth_salt        else generate_password(64))
            text = replace_php_define(   text, 'SECURE_AUTH_KEY',  self._secure_auth_key  if self._secure_auth_key  else generate_password(64))
            text = replace_php_define(   text, 'SECURE_AUTH_SALT', self._secure_auth_salt if self._secure_auth_salt else generate_password(64))
            text = replace_php_define(   text, 'LOGGED_IN_KEY',    self._logged_in_key    if self._logged_in_key    else generate_password(64))
            text = replace_php_define(   text, 'LOGGED_IN_SALT',   self._logged_in_salt   if self._logged_in_salt   else generate_password(64))
            text = replace_php_define(   text, 'NONCE_KEY',        self._nonce_key        if self._nonce_key        else generate_password(64))
            text = replace_php_define(   text, 'NONCE_SALT',       self._nonce_salt       if self._nonce_salt       else generate_password(64))
            text = replace_php_variable( text, 'table_prefix',     self._table_prefix     if self._table_prefix     else 'wp_')

        # let wordpress believe that it is talking SSL itself, if a SSL termination proxy has stripped off the SSL layer
        text_to_insert = "" \
            "if($_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https') {" \
            "    $_SERVER['HTTPS'] = 'on';" \
            "    $_SERVER['SERVER_PORT'] = 443;" \
            "}"
        end_of_config_section = text.find('/* That\'s all, stop editing! Happy blogging. */')
        text = text[:end_of_config_section] + text_to_insert + text[end_of_config_section:]
        
        # write configuraton file
        # ---------------------------------------------------------------------------------------
        write_text_file(CONFIGURATION_FILE_PATH, 'utf-8', text)


    # -------------------------------------------------------------------------------------------




