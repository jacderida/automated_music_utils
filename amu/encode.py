import os
import subprocess
from amu.config import ConfigurationError
from amu.config import ConfigurationProvider


class LameEncoder(object):
    def __init__(self, config_provider):
        if config_provider is None:
            config_provider = ConfigurationProvider()
        self._config_provider = config_provider

    def encode_wav_to_mp3(self, source, destination):
        if not os.path.exists(source):
            raise ConfigurationError('The source to encode does not exist')
        if os.path.isdir(source):
            raise ConfigurationError('The source should not be a directory')
        subprocess_args = [
            self._config_provider.get_lame_path(),
            self._config_provider.get_encoding_setting(),
            source,
            destination
        ]
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            if line:
                print "[encode] {0}".format(line.strip())
