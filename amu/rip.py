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
        popen = subprocess.Popen(
            [self._config_provider, '-d'], stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            print line
