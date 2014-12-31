#!/usr/bin/env python
import argparse
import sys
from amu.commands.ripcdcommand import RipCdCommand


def main():
    driver = CliDriver()
    return driver.main()

class CliDriver(object):
    def get_argument_parser(self):
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
        self._get_arguments()
        return 0

class CommandParser(object):
    """ Responsible for parsing the string based command from the command line
        into a command object that can be executed.
    """
    def from_args(self, args):
        return RipCdCommand()

if __name__ == '__main__':
    sys.exit(main())
