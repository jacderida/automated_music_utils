import ConfigParser
import os
import subprocess
from amu.config import ConfigurationProvider


class RubyRipperCdRipper(object):
    def __init__(self, config_provider):
        if config_provider is None:
            config_provider = ConfigurationProvider()
        self._config_provider = config_provider

    def rip_cd(self):
        subprocess_args = [
            self._config_provider.get_ruby_ripper_path(),
            '-c',
            self._config_provider.get_ruby_ripper_config_file()
        ]
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            print line
