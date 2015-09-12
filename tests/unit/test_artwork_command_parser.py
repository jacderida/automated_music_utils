import mock
import unittest
from mock import Mock
from amu.commands import AddArtworkCommand
from amu.parsing import ArtworkCommandParser

class ArtworkCommandParserTest(unittest.TestCase):
    def test__parse_add_artwork_command__source_is_file__an_add_artwork_command_should_be_returned(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertIsInstance(commands[0], AddArtworkCommand)

    def test__parse_add_artwork_command__source_is_file__add_artwork_command_should_have_source_specified_correctly(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual(source, commands[0].source)

    def test__parse_add_artwork_command__source_is_file__add_artwork_command_should_have_destination_specified_correctly(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual(destination, commands[0].destination)

    @mock.patch('os.path.isdir')
    def test__parse_add_artwork_command__source_is_directory_with_cover_jpg__add_artwork_command_should_have_source_set_as_cover_jpg(self, isdir_mock):
        source = '/some/source'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.return_value = True
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/cover.jpg', commands[0].source)
