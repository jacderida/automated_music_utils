import ConfigParser
import os
import re
import subprocess
import tempfile
import uuid


class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError, self).__init__(message)
        self.message = message

class ConfigurationProvider(object):
    def __init__(self, mask_replacer):
        self._mask_replacer = mask_replacer

    def get_lame_path(self):
        if not subprocess.call(['which', 'lame']):
            return 'lame'
        path_from_env_variable = os.environ.get('LAME_PATH')
        if path_from_env_variable:
            return self._get_verified_path_from_environment_variable(path_from_env_variable, 'LAME_PATH', 'lame')
        return self._get_verified_path_from_config_file('encoding', 'lame_path', 'lame')

    def get_flac_path(self):
        if not subprocess.call(['which', 'flac']):
            return 'flac'
        path_from_env_variable = os.environ.get('FLAC_PATH')
        if path_from_env_variable:
            return self._get_verified_path_from_environment_variable(path_from_env_variable, 'FLAC_PATH', 'flac')
        return self._get_verified_path_from_config_file('encoding', 'flac_path', 'flac')

    def get_lame_encoding_setting(self):
        config = self._get_config_parser()
        encoding_setting = config.get('encoding', 'lame_encoding_setting')
        if not encoding_setting:
            raise ConfigurationError('A value must be provided for the lame encoding setting.')
        return encoding_setting

    def get_flac_encoding_setting(self):
        config = self._get_config_parser()
        encoding_setting = config.get('encoding', 'flac_encoding_setting')
        if not encoding_setting:
            raise ConfigurationError('A value must be provided for the flac encoding setting.')
        return encoding_setting

    def get_flac_decode_setting(self):
        config = self._get_config_parser()
        decode_setting = config.get('encoding', 'flac_decode_setting')
        if not decode_setting:
            raise ConfigurationError('A value must be provided for the flac decode setting.')
        return decode_setting

    def get_ruby_ripper_path(self):
        if not subprocess.call(['which', 'rubyripper_cli']):
            return 'rubyripper_cli'
        path_from_env_variable = os.environ.get('RUBYRIPPER_CLI_PATH')
        if path_from_env_variable:
            return self._get_verified_path_from_environment_variable(
                path_from_env_variable, 'RUBYRIPPER_CLI_PATH', 'ruby ripper')
        return self._get_verified_path_from_config_file('ripper', 'path', 'ruby ripper')

    def get_ruby_ripper_config_file(self):
        path_from_env_variable = os.environ.get('RUBYRIPPER_CONFIG_PATH')
        if not os.path.exists(path_from_env_variable):
            raise ConfigurationError(
                'The path specified by RUBYRIPPER_CONFIG_PATH is incorrect. Please provide a valid path for ruby ripper.')
        return path_from_env_variable

    def get_temp_config_file_for_ripper(self, destination_path):
        if not destination_path:
            raise ConfigurationError('A destination path must be specified for the CD rip.')
        config_path = self.get_ruby_ripper_config_file()
        temp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
        with open(temp_path, 'w') as config_file:
            for line in lines:
                config_file.write(re.sub('REPLACE_BASE_DIR', destination_path, line))
        return temp_path

    def get_releases_destination_with_mask_replaced(self, release_model):
        config = self._get_config_parser()
        replaced_mask = self._mask_replacer.replace_directory_mask(config.get('masks', 'default'), release_model)
        releases_base_directory = os.path.expanduser(config.get('directories', 'releases_base_directory'))
        return os.path.join(releases_base_directory, replaced_mask)

    def get_mixes_destination(self):
        config = self._get_config_parser()
        mixes_directory = os.path.expanduser(config.get('directories', 'mixes_directory'))
        if not mixes_directory:
            raise ConfigurationError('A value must be supplied in the .amu_config file for the mixes directory.')
        return mixes_directory

    def _get_verified_path_from_environment_variable(self, path_from_env_variable, env_variable_name, program):
        if not os.path.exists(path_from_env_variable):
            raise ConfigurationError(
                'The path specified by {0} is incorrect. Please provide a valid path for {1}.'.format(env_variable_name, program))
        return path_from_env_variable

    def _get_verified_path_from_config_file(self, config_section, config_value, program):
        config = self._get_config_parser()
        path_from_config = config.get(config_section, config_value)
        if not os.path.exists(path_from_config):
            raise ConfigurationError(
                'The path specified to {0} in the .amu_config file is incorrect. Please provide a valid path for {0}.'.format(program))
        return path_from_config

    def _get_config_parser(self):
        config = ConfigParser.ConfigParser()
        config_path = os.path.join(os.path.expanduser('~'), '.amu_config')
        if not os.path.exists(config_path):
            raise ConfigurationError('The .amu_config file does not exist in your home directory.')
        config.read(config_path)
        return config
