import ConfigParser
import os
import subprocess


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
            if not os.path.exists(path_from_env_variable):
                raise ConfigurationError(
                    """The path specified by RUBYRIPPER_CLI_PATH
                    is incorrect. Please provide a valid path for
                    ruby ripper.""")
            return path_from_env_variable
        config = ConfigParser.ConfigParser()
        config_path = os.path.join(os.path.expanduser('~'), '.amu_config')
        if not os.path.exists(config_path):
            raise ConfigurationError(
                """The path specified to ruby ripper in the .amu_config
                file is incorrect. Please provide a valid path for
                ruby ripper.""")
        config.read(config_path)
        path_from_config = config.get('ripper', 'path')
        if path_from_config:
            if not os.path.exists(path_from_config):
                raise ConfigurationError(
                    """The path specified to ruby ripper in the .amu_config
                    file is incorrect. Please provide a valid path for
                    ruby ripper.""")
            return path_from_config
