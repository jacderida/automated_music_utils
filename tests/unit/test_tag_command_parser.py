import mock
import unittest
from amu.commands import AddMp3TagCommand
from amu.parsing import TagCommandParser


class TagCommandParserTest(unittest.TestCase):
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file__returns_single_add_mp3_tag_command(self, config_mock):
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command('/some/path/to/song.mp3')
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], AddMp3TagCommand)
        self.assertEqual('/some/path/to/song.mp3', commands[0].source)
