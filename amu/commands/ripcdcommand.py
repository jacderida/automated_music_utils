from amu.commands.command import Command
from amu.rip import RubyRipperCdRipper


class RipCdCommand(Command):
    def __init__(self, cd_ripper):
        if cd_ripper is None:
            cd_ripper = RubyRipperCdRipper()
        self._cd_ripper = cd_ripper

    def execute(self):
        self._cd_ripper.rip_cd()
