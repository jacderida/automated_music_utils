import unittest
from mock import Mock
from amu.commands.command import CommandValidationError
from amu.commands.ripcdcommand import RipCdCommand


class RipCdCommandTest(unittest.TestCase):
    def test_execute_calls_cd_ripper_rip_cd(self):
        cd_ripper = Mock()
        command = RipCdCommand(cd_ripper)
        command.execute()
        cd_ripper.rip_cd.assert_called_once_with()

    def test_execute_throws_when_cd_ripper_is_not_installed(self):
        cd_ripper = Mock()
        cd_ripper.is_installed.return_value = False
        command = RipCdCommand(cd_ripper)
        with self.assertRaises(CommandValidationError):
            command.execute()
