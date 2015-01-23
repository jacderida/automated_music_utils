import os
import subprocess
import tempfile
from amu.config import ConfigurationProvider


class RubyRipperCdRipper(object):
    def __init__(self, config_provider):
        if config_provider is None:
            config_provider = ConfigurationProvider()
        self._config_provider = config_provider

    def rip_cd(self):
        temp_path = os.path.join(tempfile.gettempdir(), 'random')
        os.mkdir(temp_path)
        subprocess_args = [
            self._config_provider.get_ruby_ripper_path(),
            '--defaults',
            '--file',
            self._config_provider.get_temp_config_file_for_ripper('destination')
        ]
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            print line
