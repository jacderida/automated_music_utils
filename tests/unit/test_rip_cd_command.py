import unittest
from mock import Mock
from amu.commands.ripcdcommand import RipCdCommand


class RipCdCommandTest(unittest.TestCase):
    def test_execute_calls_cd_ripper_rip_cd(self):
        cd_ripper = Mock()
        command = RipCdCommand(cd_ripper)
        command.execute()
        cd_ripper.rip_cd.assert_called_once_with()
