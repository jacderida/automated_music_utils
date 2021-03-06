import mock
import unittest
from mock import Mock
from amu.commands import CommandValidationError
from amu.commands import RipCdCommand


class RipCdCommandTest(unittest.TestCase):
    def test__execute__calls_rip_cd_with_correct_destination__cd_ripper_called_once(self):
        config_mock, cd_ripper_mock = (Mock(),)*2
        command = RipCdCommand(config_mock, cd_ripper_mock)
        command.destination = '/some/path'
        command.execute()
        cd_ripper_mock.rip_cd.assert_called_once_with('/some/path')

    def test__validate__destination_is_empty__throws_command_validation_exception(self):
        with self.assertRaises(CommandValidationError):
            config_mock, cd_ripper_mock = (Mock(),)*2
            command = RipCdCommand(config_mock, cd_ripper_mock)
            command.validate()
