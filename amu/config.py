import ConfigParser
import os
import subprocess
import uuid


class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)
        self.message = message

class ConfigurationProvider(object):
    def get_ruby_ripper_path(self):
        if not subprocess.call(['which', 'rubyripper_cli']):
            return 'rubyripper_cli'
        path_from_env_variable = os.environ.get('RUBYRIPPER_CLI_PATH')
        if path_from_env_variable:
            return self._get_verified_path_from_environment_variable(path_from_env_variable)
        return self._get_verified_path_from_config_file()

    def get_ruby_ripper_config_file(self):
        path_from_env_variable = os.environ.get('RUBYRIPPER_CONFIG_PATH')
        if not os.path.exists(path_from_env_variable):
            raise ConfigurationError(
                """The path specified by RUBYRIPPER_CONFIG_PATH
                is incorrect. Please provide a valid path for
                ruby ripper.""")
        return path_from_env_variable

    def get_temp_config_path_for_ripper(self):
        config_path = self.get_ruby_ripper_config_file()
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        path_from_config = config.get('ripper', 'temp_path')
        temp_path = os.path.join(path_from_config, str(uuid.uuid4()))
        return temp_path

    def _get_verified_path_from_environment_variable(self, path_from_env_variable):
        if not os.path.exists(path_from_env_variable):
            raise ConfigurationError(
                """The path specified by RUBYRIPPER_CLI_PATH
                is incorrect. Please provide a valid path for
                ruby ripper.""")
        return path_from_env_variable

    def _get_verified_path_from_config_file(self):
        config = ConfigParser.ConfigParser()
        config_path = os.path.join(os.path.expanduser('~'), '.amu_config')
        if not os.path.exists(config_path):
            raise ConfigurationError(
                'The .amu_config file does not exist in your home directory.')
        config.read(config_path)
        path_from_config = config.get('ripper', 'path')
        if not os.path.exists(path_from_config):
            raise ConfigurationError(
                """The path specified to ruby ripper in the .amu_config
                file is incorrect. Please provide a valid path for
                ruby ripper.""")
        return path_from_config
