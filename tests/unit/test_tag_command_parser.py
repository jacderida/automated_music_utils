import mock
import unittest
from amu.commands import AddMp3TagCommand
from amu.parsing import TagCommandParser


class TagCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file__returns_single_add_mp3_tag_command(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command('/some/path/to/song.mp3')
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], AddMp3TagCommand)
        self.assertEqual('/some/path/to/song.mp3', commands[0].source)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_4_mp3s__returns_4_correctly_specified_add_mp3_tag_commands(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isfile_mock.return_value = False
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command('/some/path/to/mp3s')
        self.assertEqual(4, len(commands))
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)
