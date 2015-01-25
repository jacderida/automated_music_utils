""" Test suite for the command parser. """
import mock
import os
import unittest
from amu.clidriver import CliDriver
from amu.clidriver import CommandParser
from amu.commands.ripcdcommand import RipCdCommand


class CommandParserTest(unittest.TestCase):
    """ Test suite for the command parser. """
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_rip_cd_is_specified__command_parser_returns_rip_cd_command(self, config_mock, cd_ripper_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock)
        command = parser.from_args(args)
        self.assertIsInstance(command, RipCdCommand)

    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__rip_cd_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock)
        command = parser.from_args(args)
        self.assertEqual(os.getcwd(), command.destination)
