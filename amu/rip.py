import ConfigParser
import os
import subprocess


class RubyRipperCdRipper(object):
    def __init__(self):
        self._rubyripper_path = ''

    @property
    def rubyripper_path(self):
        return self._rubyripper_path

    def rip_cd(self):
        popen = subprocess.Popen(
            [self.rubyripper_path, '-d'], stdout=subprocess.PIPE)
        lines_iterator = iter(popen.stdout.readline, "")
        for line in lines_iterator:
            print line
