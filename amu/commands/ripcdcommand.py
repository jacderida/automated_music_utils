from amu.commands.command import Command
from amu.commands.command import CommandValidationError
from amu.rip import RubyRipperCdRipper


class RipCdCommand(Command):
    def __init__(self, config_provider, cd_ripper):
        super(RipCdCommand, self).__init__(config_provider)
        if cd_ripper is None:
            cd_ripper = RubyRipperCdRipper()
        self._cd_ripper = cd_ripper

    def validate(self):
        if not self._cd_ripper.is_installed():
            raise CommandValidationError('A CD ripper has not been configured for on this system')

    def execute(self):
        self.validate()
        self._cd_ripper.rip_cd()
