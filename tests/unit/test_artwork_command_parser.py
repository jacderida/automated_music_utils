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
