import mock
import unittest
from mock import patch
from amu.commands.command import CommandValidationError
from amu.commands.ripcdcommand import RipCdCommand


class RipCdCommandTest(unittest.TestCase):
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__execute__calls_cd_ripper_rip_cd__cd_ripper_called_once(self, config_mock, cd_ripper_mock):
        command = RipCdCommand(config_mock, cd_ripper_mock)
        command.execute()
        cd_ripper_mock.rip_cd.assert_called_once_with()
