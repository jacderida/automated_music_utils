import mock
import unittest
from amu.commands import AddTagCommand
from amu.commands import MoveAudioFileCommand
from amu.parsing import AddTagCommandArgs
from amu.parsing import CommandParsingError
from amu.parsing import MixCommandParser
from mock import Mock

class MixCommandParserTest(unittest.TestCase):
    def test__parse_mix_command__single_file_mix__it_should_generate_an_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertIsInstance(commands[0], AddTagCommand)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_artist_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].artist, 'Aphex Twin')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_artist_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album_artist, 'Aphex Twin')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album, "All Tomorrow's Parties")

    def test__parse_mix_command__single_file_mix__it_should_specify_the_title_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].title, "All Tomorrow's Parties")

    def test__parse_mix_command__single_file_mix__it_should_specify_the_year_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].year, '2003')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_comment_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].comment, "DJ Set at All Tomorrow's Parties 2003")

    def test__parse_mix_command__single_file_mix__it_should_specify_the_genre_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].genre, 'Mixes')

    def test__parse_mix_command__single_file_mix__it_should_specify_the_track_number_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].track_number, 1)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_track_total_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].track_total, 1)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_disc_number_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].disc_number, 1)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_disc_total_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].disc_total, 1)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_source_on_the_add_tag_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].source, '/some/source/track.mp3')

    def test__parse_mix_command__single_file_mix__it_should_generate_a_move_file_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertIsInstance(commands[1], MoveAudioFileCommand)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_source_on_the_move_file_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[1].source, '/some/source/track.mp3')

    def test__parse_mix_command__source_is_empty__raises_value_error(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = ''
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        with self.assertRaisesRegexp(ValueError, ''):
            mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
            mix_command_parser.parse_mix_command(tag_command_args)

    def test__parse_mix_command__single_file_mix__it_should_specify_the_destination_on_the_move_file_command(self):
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[1].destination, '/mixes/destination/track.mp3')
