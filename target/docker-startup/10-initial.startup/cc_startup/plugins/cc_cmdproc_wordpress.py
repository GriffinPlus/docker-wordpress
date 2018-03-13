"""
This module contains everything needed to configure 'WordPress'.
Author: Sascha Falk <sascha@falk-online.eu>
License: MIT License
"""

import os
import re

from configparser import ConfigParser
from pwd import getpwnam
from stat import S_IRUSR, S_IWUSR, S_IXUSR, S_IRGRP, S_IWGRP, S_IXGRP, S_IROTH, S_IWOTH, S_IXOTH

from ..cc_log import Log
from ..cc_cmdproc import CommandProcessor, PositionalArgument, NamedArgument
from ..cc_errors import GeneralError, CommandLineArgumentError, FileNotFoundError, IoError, ConfigurationError, EXIT_CODE_SUCCESS
from ..cc_helpers import read_text_file, write_text_file, replace_php_define, replace_php_variable, generate_password, get_env_setting_bool, get_env_setting_integer, get_env_setting_string


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


CONFIGURATION_FILE_PATH = "/var/www/html/wp-config.php"
SAMPLE_CONFIGURATION_FILE_PATH = "/var/www/html/wp-config-sample.php"
HTTP_SERVER_USER = "www-data"

# -------------------------------------------------------------------------------------------------------------------------------------------------------------


# name of the processor
processor_name = 'wordpress'

# determines whether the processor is run by the startup script
enabled = True

def get_processor():
    "Returns an instance of the processor provided by the command processor plugin."
    return WordPressCommandProcessor()


# -------------------------------------------------------------------------------------------------------------------------------------------------------------


class WordPressCommandProcessor(CommandProcessor):

    # -------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        # let base class perform its initialization
        super().__init__()

        # register command handlers
        self.add_handler(self.run, PositionalArgument("run"))
        self.add_handler(self.run, PositionalArgument("run-and-enter"))


    # -------------------------------------------------------------------------------------------------------------------------------------


    def run(self, pos_args, named_args):

        # load configuration file (respectively the sample configuration file, if the configuration file does not exist, yet)
        # ---------------------------------------------------------------------------------------
        if os.path.exists(CONFIGURATION_FILE_PATH):
            config_file, _ = read_text_file(CONFIGURATION_FILE_PATH, "utf-8")
            config_file_exists = True
        elif os.path.exists(SAMPLE_CONFIGURATION_FILE_PATH):
            config_file, _ = read_text_file(SAMPLE_CONFIGURATION_FILE_PATH, "utf-8")
            config_file_exists = False
        else:
           raise FileNotFoundError("Neither the configuraton file ({0}) nor the sample configuration file ({1}) exists.".format(CONFIGURATION_FILE_PATH, SAMPLE_CONFIGURATION_FILE_PATH))

        # database
        # ---------------------------------------------------------------------------------------
        db_host = get_env_setting_string("WORDPRESS_DB_HOST")
        if not db_host and not config_file_exists:
            error = "Environment variable WORDPRESS_DB_HOST is not set."
            raise ConfigurationError(error)

        db_user = get_env_setting_string("WORDPRESS_DB_USER")
        if not db_user and not config_file_exists:
            error = "Environment variable WORDPRESS_DB_USER is not set."
            raise ConfigurationError(error)

        db_password = get_env_setting_string("WORDPRESS_DB_PASSWORD")
        if not db_password and not config_file_exists:
            error = "Environment variable WORDPRESS_DB_PASSWORD is not set."
            raise ConfigurationError(error)

        db_name = get_env_setting_string("WORDPRESS_DB_NAME")
        table_prefix = get_env_setting_string("WORDPRESS_TABLE_PREFIX")

        # cryptographic keys and salts
        # ---------------------------------------------------------------------------------------

        auth_key = get_env_setting_string("WORDPRESS_AUTH_KEY")
        auth_salt = get_env_setting_string("WORDPRESS_AUTH_SALT")
        secure_auth_key = get_env_setting_string("WORDPRESS_SECURE_AUTH_KEY")
        secure_auth_salt = get_env_setting_string("WORDPRESS_SECURE_AUTH_SALT")
        logged_in_key = get_env_setting_string("WORDPRESS_LOGGED_IN_KEY")
        logged_in_salt = get_env_setting_string("WORDPRESS_LOGGED_IN_SALT")
        nonce_key = get_env_setting_string("WORDPRESS_NONCE_KEY")
        nonce_salt = get_env_setting_string("WORDPRESS_NONCE_SALT")

        # ---------------------------------------------------------------------------------------

        text = config_file

        if config_file_exists:

            # the configuration file exists, i.e. it should already contain valid settings
            # => override settings that have been specified in environment variables
            if db_host:          text = replace_php_define(   text, "DB_HOST",          db_host)
            if db_user:          text = replace_php_define(   text, "DB_USER",          db_user)
            if db_password:      text = replace_php_define(   text, "DB_PASSWORD",      db_password)
            if db_name:          text = replace_php_define(   text, "DB_NAME",          db_name)
            if auth_key:         text = replace_php_define(   text, "AUTH_KEY",         auth_key)
            if auth_salt:        text = replace_php_define(   text, "AUTH_SALT",        auth_salt)
            if secure_auth_key:  text = replace_php_define(   text, "SECURE_AUTH_KEY",  secure_auth_key)
            if secure_auth_salt: text = replace_php_define(   text, "SECURE_AUTH_SALT", secure_auth_salt)
            if logged_in_key:    text = replace_php_define(   text, "LOGGED_IN_KEY",    logged_in_key)
            if logged_in_salt:   text = replace_php_define(   text, "LOGGED_IN_SALT",   logged_in_salt)
            if nonce_key:        text = replace_php_define(   text, "NONCE_KEY",        nonce_key)
            if nonce_salt:       text = replace_php_define(   text, "NONCE_SALT",       nonce_salt)
            if table_prefix:     text = replace_php_variable( text, "table_prefix",     table_prefix)
        else:
            # the configuration file does not exist, i.e. the sample file was loaded
            # => override all settings, provide sensible defaults, if necessary)
            text = replace_php_define(   text, "DB_HOST",          db_host)         # always inited, since checked above
            text = replace_php_define(   text, "DB_USER",          db_user)         # always inited, since checked above
            text = replace_php_define(   text, "DB_PASSWORD",      db_password)     # always inited, since checked above
            text = replace_php_define(   text, "DB_NAME",          db_name          if db_name          else "wordpress")
            text = replace_php_define(   text, "AUTH_KEY",         auth_key         if auth_key         else generate_password(64))
            text = replace_php_define(   text, "AUTH_SALT",        auth_salt        if auth_salt        else generate_password(64))
            text = replace_php_define(   text, "SECURE_AUTH_KEY",  secure_auth_key  if secure_auth_key  else generate_password(64))
            text = replace_php_define(   text, "SECURE_AUTH_SALT", secure_auth_salt if secure_auth_salt else generate_password(64))
            text = replace_php_define(   text, "LOGGED_IN_KEY",    logged_in_key    if logged_in_key    else generate_password(64))
            text = replace_php_define(   text, "LOGGED_IN_SALT",   logged_in_salt   if logged_in_salt   else generate_password(64))
            text = replace_php_define(   text, "NONCE_KEY",        nonce_key        if nonce_key        else generate_password(64))
            text = replace_php_define(   text, "NONCE_SALT",       nonce_salt       if nonce_salt       else generate_password(64))
            text = replace_php_variable( text, "table_prefix",     table_prefix     if table_prefix     else "wp_")

            # let wordpress believe that it is talking SSL itself, if a SSL termination proxy has stripped off the SSL layer
            text_to_insert = "" \
                "if($_SERVER['HTTP_X_FORWARDED_PROTO'] == 'https') {\n" \
                "    $_SERVER['HTTPS'] = 'on';\n" \
                "    $_SERVER['SERVER_PORT'] = 443;\n" \
                "}\n"
            end_of_config_section = text.find("/* That's all, stop editing! Happy blogging. */")
            text = text[:end_of_config_section] + text_to_insert + text[end_of_config_section:]

        # write configuraton file
        # ---------------------------------------------------------------------------------------
        write_text_file(CONFIGURATION_FILE_PATH, "utf-8", text)

        # fix permissions
        # ---------------------------------------------------------------------------------------
        path = "/var/www"
        nginx_uid = getpwnam(HTTP_SERVER_USER).pw_uid
        nginx_gid = getpwnam(HTTP_SERVER_USER).pw_gid
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                path = os.path.join(root, dir)
                os.chown(path, nginx_uid, nginx_gid)
                os.chmod(path, S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP)
            for file in files:
                path = os.path.join(root, file)
                os.chown(path, nginx_uid, nginx_gid)
                os.chmod(path, S_IRUSR | S_IWUSR | S_IRGRP)

        return EXIT_CODE_SUCCESS


    # -------------------------------------------------------------------------------------------------------------------------------------
