""" Test suite for the command parser. """
import argparse
import mock
import unittest
from mock import patch
from amu.clidriver import CliDriver
from amu.clidriver import CommandParser
from amu.commands.ripcdcommand import RipCdCommand


class CommandParserTest(unittest.TestCase):
    """ Test suite for the command parser. """
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test_command_parser_returns_rip_cd_command(self, config_mock, cd_ripper_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock)
        command = parser.from_args(args)
        self.assertIsInstance(command, RipCdCommand)
