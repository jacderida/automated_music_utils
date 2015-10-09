import mock
import unittest
from amu.commands import AddTagCommand
from amu.parsing import AddTagCommandArgs
from amu.parsing import MixCommandParser
from mock import Mock

class MixCommandParserTest(unittest.TestCase):
    def test__parse_mix_command__single_file_mix__it_should_generate_an_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertIsInstance(commands[0], AddTagCommand)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_artist_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].artist, 'Aphex Twin')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_artist_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album_artist, 'Aphex Twin')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album, "All Tomorrow's Parties")

    def test__parse_mix_command__single_file_mix__it_should_specify_the_title_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].title, "All Tomorrow's Parties")
