#!/usr/bin/env python
import argparse
import sys
from amu.commands.ripcdcommand import RipCdCommand
from amu.config import ConfigurationProvider
from amu.rip import RubyRipperCdRipper


def main():
    driver = CliDriver()
    return driver.main()

class CliDriver(object):
    def get_argument_parser(self):
        """ Gets the standard argument parser. This is public because it will
        be useful for unit testing the command parser. """
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')
        subparsers.add_parser('rip', help='rips the current CD to WAV')
        search_parser = subparsers.add_parser(
            'search',
            prog='search',
            help='performs a very simple search on discogs')
        search_parser.add_argument('term', help='the term to search for')
        encode_parser = subparsers.add_parser(
            'encode', help='encodes a CD or a set of WAV files to mp3')
        encode_parser.add_argument(
            'source', choices=['cd', 'wav'], help='the source to encode from')
        encode_parser.add_argument(
            'releaseid', type=int, help='the ID of the discogs release')
        return parser

    def _get_arguments(self):
        parser = self.get_argument_parser()
        return parser.parse_args()

    def main(self):
        """ The main entry point for the CLI driver """
        parser = CommandParser(ConfigurationProvider(), RubyRipperCdRipper())
        command = parser.from_args(self._get_arguments())
        command.execute()
        return 0

class CommandParser(object):
    """ Responsible for parsing the string based command from the command line
        into a command object that can be executed.
    """
    def __init__(self, configuration_provider, cd_ripper):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper

    def from_args(self, args):
        return RipCdCommand(self._configuration_provider, self._cd_ripper)

if __name__ == '__main__':
    sys.exit(main())
