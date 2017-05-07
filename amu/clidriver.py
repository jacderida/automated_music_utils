#!/usr/bin/env python
import argparse
import sys
from amu.audio import LameEncoder, RubyRipperCdRipper
from amu.config import ConfigurationProvider
from amu.metadata import DiscogsMetadataService
from amu.metadata import MaskReplacer
from amu.parsing import CommandParser


class CliDriver(object):
    def get_argument_parser(self):
        """ Gets the standard argument parser. This is public because it will
        be useful for unit testing the command parser. """
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')
        fetch_parser = subparsers.add_parser('fetch', help='fetches and displays a release from discogs')
        fetch_parser.add_argument('discogs_id', help='the ID of the release')
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
            '--collapse-index-tracks', action='store_true', help='If set this will collapse any subtracks to a single track.')
        encode_parser.add_argument(
            '--discogs-id', help='The discogs ID for the release. When this is used metadata from the discogs release will be applied to the encoded files.')
        decode_parser = subparsers.add_parser('decode', help='Decodes a set of FLAC or MP3 files to WAV.')
        decode_parser.add_argument(
            'decode_from', choices=['flac', 'mp3'], help='The source to decode from.')
        decode_parser.add_argument(
            '--source', help='The destination of the source file. This can be a file or directory.')
        decode_parser.add_argument(
            '--destination', help='The destination of the resulting wav. This can be a file or directory.')
        tag_parser = subparsers.add_parser('tag', help='Tags an audio file')
        tag_parser.add_argument(
            'action', choices=['add', 'remove'], help='The tagging action to be performed. A tag can be added or removed.')
        tag_parser.add_argument(
            'format', choices=['mp3', 'flac'], help='The file format of the audio file being tagged.')
        tag_parser.add_argument(
            '--collapse-index-tracks', action='store_true', help='If set this will collapse any subtracks to a single track.')
        tag_parser.add_argument(
            '--source',
            help='The source audio files to tag. This can be a file or a directory. If the source is omitted, the files in the current working directory will be used.')
        tag_parser.add_argument('--discogs-id', help='The discogs ID for the release. When this is used metadata from the discogs release will be applied to the tagged files.')
        tag_parser.add_argument('--artist', help='The artist to use for the tag.')
        tag_parser.add_argument('--album-artist', help='The album artist to use for the tag.')
        tag_parser.add_argument('--album', help='The album to use for the tag.')
        tag_parser.add_argument('--title', help='The title to use for the tag.')
        tag_parser.add_argument('--year', help='The year to use for the tag.')
        tag_parser.add_argument('--genre', help='The year to use for the tag.')
        tag_parser.add_argument('--track-number', help='The track number to use for the tag.')
        tag_parser.add_argument('--track-total', help='The track total to use for the tag.')
        tag_parser.add_argument('--disc-number', help='The disc number to use for the tag.')
        tag_parser.add_argument('--disc-total', help='The disc total to use for the tag.')
        tag_parser.add_argument('--comment', help='The comment for the tag.')
        artwork_parser = subparsers.add_parser('artwork', help='adds or removes artwork from a file')
        artwork_parser.add_argument(
            'action', choices=['add', 'remove'], help='The artwork action to be performed. The artwork can be added or removed.')
        artwork_parser.add_argument(
            'type', choices=['mp3', 'flac'], help='The type of file to apply the artwork to.')
        artwork_parser.add_argument(
            '--source', help='The destination file or directory to apply the artwork to. If there is no source then any artwork in the current directory will be used.')
        artwork_parser.add_argument(
            '--destination', help='The destination file or directory to apply the artwork to. If there is no destination then the current directory will be used.')
        mix_parser = subparsers.add_parser('mix', help='adds a mix')
        mix_parser.add_argument('source', help='the source of the mix')
        mix_parser.add_argument('--artist', help='The artist to use for the tag.')
        mix_parser.add_argument('--album', help='The album to use for the mix.')
        mix_parser.add_argument('--title', help='The title to use for the mix.')
        mix_parser.add_argument('--year', help='The year to use for the mix.')
        mix_parser.add_argument('--comment', help='The comment for the mix.')
        return parser

    def _get_arguments(self):
        parser = self.get_argument_parser()
        return parser.parse_args()

    def main(self):
        """ The main entry point for the CLI driver """
        try:
            config_provider = ConfigurationProvider(MaskReplacer(), DirectorySelector())
            parser = CommandParser(
                config_provider,
                RubyRipperCdRipper(config_provider),
                DiscogsMetadataService(),
                GenreSelector())
            commands = parser.from_args(self._get_arguments())
            for command in commands:
                command.validate()
                command.execute()
            return 0
        except Exception as ex:
            # This will be replaced with proper logging output.
            sys.stderr.write('{0}\n'.format(ex.message))
            return 255

class DirectorySelector(object):
    def select_directory(self, directories):
        if len(directories) == 1:
            return 0
        count = 1
        print 'Select the directory for the release:'
        for directory in directories:
            print '{0}. {1}'.format(count, directory)
            count += 1
        numeric_selection = self._get_valid_input(len(directories))
        return numeric_selection - 1

    def _get_valid_input(self, length):
        while True:
            selection = self._get_input()
            try:
                numeric_selection = int(selection)
                if numeric_selection < 1 or numeric_selection > length:
                    raise ValueError
                return numeric_selection
            except ValueError:
                print 'Please enter a value between 1 and {0}.'.format(length)

    def _get_input(self):
        return raw_input()

class GenreSelector(object):
    def select_genre(self, genres):
        count = 1
        print "Select the genre from what's available from the discogs release, or provide a free text value:"
        for genre in genres:
            print u'{0}. {1}'.format(count, genre)
            count += 1
        return self._get_selection(genres)

    def _get_selection(self, genres):
        while True:
            selection = self._get_input()
            try:
                numeric_selection = int(selection)
                if numeric_selection < 1 or numeric_selection > len(genres):
                    print 'Please enter a value between 1 and {0}.'.format(len(genres))
                    continue
                return genres[numeric_selection - 1]
            except ValueError:
                    return selection

    def _get_input(self):
        return raw_input()

def main():
    driver = CliDriver()
    return driver.main()

if __name__ == '__main__':
    sys.exit(main())
