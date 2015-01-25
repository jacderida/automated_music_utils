from amu.commands.command import Command
from amu.commands.command import CommandValidationError
from amu.rip import RubyRipperCdRipper


class RipCdCommand(Command):
    def __init__(self, config_provider, cd_ripper):
        super(RipCdCommand, self).__init__(config_provider)
        if cd_ripper is None:
            cd_ripper = RubyRipperCdRipper(config_provider)
        self._cd_ripper = cd_ripper
        self._destination = ''

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    def execute(self):
        self.validate()
        self._cd_ripper.rip_cd()
