import mock
import unittest
from amu.commands import AddMp3TagCommand
from amu.parsing import AddTagCommandArgs
from amu.parsing import TagCommandParser


class TagCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file__returns_single_add_mp3_tag_command(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], AddMp3TagCommand)
        self.assertEqual('/some/path/to/song.mp3', commands[0].source)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__artist_is_specified__add_mp3_tag_command_has_artist_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Aphex Twin', commands[0].artist)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__album_is_specified__add_mp3_tag_command_has_album_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Druqks', commands[0].album)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__title_is_specified__add_mp3_tag_command_has_title_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Vordhosbn', commands[0].title)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_no_track_number_is_specified__add_mp3_tag_command_has_track_number_set_to_1(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(1, commands[0].track_number)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_4_mp3s__returns_4_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(4, len(commands))
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)
