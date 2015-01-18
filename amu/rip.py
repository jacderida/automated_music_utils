import ConfigParser
import os
import re
import subprocess
from amu.config import ConfigurationProvider


class RubyRipperCdRipper(object):
    def __init__(self, config_provider):
        if config_provider is None:
            config_provider = ConfigurationProvider()
        self._config_provider = config_provider

    def rip_cd(self):
        config_path = self._config_provider.get_ruby_ripper_config_file()
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
        with open(config_path, 'w') as config_file:
            for line in lines:
                config_file.write(re.sub('REPLACE_BASE_DIR', '/tmp/rip', line))
        subprocess_args = [
            self._config_provider.get_ruby_ripper_path(),
            '--defaults',
            '--file',
            config_path
        ]
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            print line
