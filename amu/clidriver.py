#!/usr/bin/env python
import argparse
import sys
from amu.config import ConfigurationProvider
from amu.encode import LameEncoder
from amu.metadata import DiscogsMetadataService
from amu.metadata import MaskReplacer
from amu.parsing import CommandParser
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
        rip_parser = subparsers.add_parser('rip', help='rips the current CD to WAV')
        rip_parser.add_argument('--destination', help='optional destination for the CD rip')
        search_parser = subparsers.add_parser(
            'search',
            prog='search',
            help='performs a very simple search on discogs')
        search_parser.add_argument('term', help='the term to search for')
        encode_parser = subparsers.add_parser(
            'encode', help='Encodes a CD or a set of WAV files to mp3.')
        encode_parser.add_argument(
            'encoding_from', choices=['cd', 'wav'], help='The source to encode from.')
        encode_parser.add_argument(
            'encoding_to', choices=['mp3', 'flac'], help='The destination to encode to.')
        encode_parser.add_argument(
            '--source', help='The destination of the source wav file. This can be a file or directory.')
        encode_parser.add_argument(
            '--destination', help='The destination of the resulting mp3 or flac. This can be a file or directory.')
        encode_parser.add_argument(
            '--keep-source', action='store_true', help='If encoding from wav, use this to keep the original wav being removed.')
        encode_parser.add_argument(
            '--discogs-id', help='The discogs ID for the release. When this is used metadata from the discogs release will be applied to the encoded files.')
        tag_parser = subparsers.add_parser('tag', help='Tags an audio file')
        tag_parser.add_argument(
            'action', choices=['add', 'remove'], help='The tagging action to be performed. A tag can be added or removed.')
        tag_parser.add_argument(
            'format', choices=['mp3', 'flac'], help='The file format of the audio file being tagged.')
        tag_parser.add_argument(
            '--source',
            help='The source audio files to tag. This can be a file or a directory. If the source is omitted, the files in the current working directory will be used.')
        tag_parser.add_argument('--artist', help='The artist to use for the tag.')
        tag_parser.add_argument('--album', help='The album to use for the tag.')
        tag_parser.add_argument('--title', help='The title to use for the tag.')
        tag_parser.add_argument('--year', help='The year to use for the tag.')
        tag_parser.add_argument('--genre', help='The year to use for the tag.')
        tag_parser.add_argument('--track-number', help='The track number to use for the tag.')
        tag_parser.add_argument('--track-total', help='The track total to use for the tag.')
        tag_parser.add_argument('--comment', help='The comment for the tag.')
        return parser

    def _get_arguments(self):
        parser = self.get_argument_parser()
        return parser.parse_args()

    def main(self):
        """ The main entry point for the CLI driver """
        config_provider = ConfigurationProvider(MaskReplacer())
        parser = CommandParser(
            config_provider,
            RubyRipperCdRipper(config_provider),
            LameEncoder(config_provider),
            DiscogsMetadataService())
        commands = parser.from_args(self._get_arguments())
        for command in commands:
            command.validate()
            command.execute()
        return 0

if __name__ == '__main__':
    sys.exit(main())
