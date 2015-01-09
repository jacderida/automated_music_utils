import ConfigParser
import os
import subprocess


class ConfigurationProvider(object):
    def get_ruby_ripper_path(self):
        if not subprocess.call(['which', 'rubyripper_cli']):
            return 'rubyripper_cli'
        path_from_env_variable = os.environ.get('RUBYRIPPER_CLI_PATH')
        if path_from_env_variable:
            return path_from_env_variable
        config = ConfigParser.ConfigParser()
        config_path = os.path.join(os.path.expanduser('~'), '.amu_config')
        config.read(config_path)
        path_from_config = config.get('ripper', 'path')
        if path_from_config:
            return path_from_config
