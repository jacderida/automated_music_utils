import mock
import unittest
from mock import patch
from amu.commands.command import CommandValidationError
from amu.commands.ripcdcommand import RipCdCommand


class RipCdCommandTest(unittest.TestCase):
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test_execute_calls_cd_ripper_rip_cd(self, config_mock, cd_ripper_mock):
        command = RipCdCommand(config_mock, cd_ripper_mock)
        command.execute()
        cd_ripper_mock.rip_cd.assert_called_once_with()

    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test_execute_throws_when_cd_ripper_is_not_installed(self, config_mock, cd_ripper_mock):
        cd_ripper_mock.is_installed.return_value = False
        command = RipCdCommand(config_mock, cd_ripper_mock)
        with self.assertRaises(CommandValidationError):
            command.execute()
