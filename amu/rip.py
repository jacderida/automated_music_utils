import os
import shutil
import subprocess
import tempfile
import uuid
from amu import utils
from amu.config import ConfigurationError
from amu.config import ConfigurationProvider


class RubyRipperCdRipper(object):
    def __init__(self, config_provider):
        if config_provider is None:
            config_provider = ConfigurationProvider()
        self._config_provider = config_provider

    def rip_cd(self, destination):
        if not destination:
            raise ConfigurationError('A destination must be provided for the CD rip')
        expanded_destination = os.path.expanduser(destination)
        if not os.path.exists(expanded_destination):
            os.mkdir(expanded_destination)
        temp_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        temp_config_path = self._config_provider.get_temp_config_file_for_ripper(temp_path)
        subprocess_args = [
            self._config_provider.get_ruby_ripper_path(),
            '--defaults',
            '--file',
            temp_config_path
        ]
        print "[rip] Running rubyripper with {0}".format(subprocess_args)
        popen = subprocess.Popen(subprocess_args, stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            if line:
                print "[rip] {0}".format(line.strip())
        utils.copy_content_to_directory(temp_path, expanded_destination)
        shutil.rmtree(temp_path)
        os.remove(temp_config_path)
