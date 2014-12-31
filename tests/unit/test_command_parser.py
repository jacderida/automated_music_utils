""" Test suite for the command parser. """
import argparse
import unittest
from amu.clidriver import CliDriver
from amu.clidriver import CommandParser

class CommandParserTest(unittest.TestCase):
    """ Test suite for the command parser. """
    def test_command_parser_returns_rip_cd_command(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser()
        command = parser.from_args(args)
        self.assertIsNotNone(command)
