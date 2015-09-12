import mock
import unittest
from mock import Mock
from amu.commands import AddArtworkCommand
from amu.parsing import ArtworkCommandParser
from amu.parsing import CommandParsingError

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
    @mock.patch('os.listdir')
    def test__parse_add_artwork_command__source_is_directory_with_cover_jpg__add_artwork_command_should_have_source_set_as_cover_jpg(self, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.return_value = True
        listdir_mock.return_value = ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.jpg']
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/cover.jpg', commands[0].source)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    def test__parse_add_artwork_command__source_is_directory_with_cover_png__add_artwork_command_should_have_source_set_as_cover_jpg(self, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.return_value = True
        listdir_mock.return_value = ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.png']
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/cover.png', commands[0].source)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    def test__parse_add_artwork_command__source_is_directory_with_no_covers__raises_command_parsing_error(self, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.return_value = True
        listdir_mock.return_value = ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3']
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory contains no cover jpg or png.'):
            parser = ArtworkCommandParser(config_mock, tagger_mock)
            parser.parse_add_artwork_command(source, destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_directory__returns_3_add_artwork_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/source'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [('/some/source', (), ('01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3'))]
        listdir_mock.side_effect = [['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.jpg']]
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual(3, len(commands))

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_directory__destination_should_be_set_correctly_on_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/source'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [('/some/source', (), ('01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3'))]
        listdir_mock.return_value = ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.jpg']
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/01 - Track 01.mp3', commands[0].destination)
        self.assertEqual('/some/source/02 - Track 02.mp3', commands[1].destination)
        self.assertEqual('/some/source/03 - Track 03.mp3', commands[2].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_multi_cd__destination_should_be_set_correctly_on_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/source'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [
            ('/some/source', ('cd1', 'cd2'), ()),
            ('/some/source/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3')),
            ('/some/source/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.jpg'],
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3'],
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3']
        ]
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/cd1/01 - Track 01.mp3', commands[0].destination)
        self.assertEqual('/some/source/cd1/02 - Track 02.mp3', commands[1].destination)
        self.assertEqual('/some/source/cd1/03 - Track 03.mp3', commands[2].destination)
        self.assertEqual('/some/source/cd2/01 - Track 01.mp3', commands[3].destination)
        self.assertEqual('/some/source/cd2/02 - Track 02.mp3', commands[4].destination)
        self.assertEqual('/some/source/cd2/03 - Track 03.mp3', commands[5].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_multi_cd__source_should_be_set_correctly_on_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/source'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [
            ('/some/source', ('cd1', 'cd2'), ()),
            ('/some/source/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3')),
            ('/some/source/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3', 'cover.jpg'],
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3'],
            ['01 - Track 01.mp3', '02 - Track 02.mp3', '03 - Track 03.mp3']
        ]
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination)
        self.assertEqual('/some/source/cover.jpg', commands[0].source)
        self.assertEqual('/some/source/cover.jpg', commands[1].source)
        self.assertEqual('/some/source/cover.jpg', commands[2].source)
        self.assertEqual('/some/source/cover.jpg', commands[3].source)
        self.assertEqual('/some/source/cover.jpg', commands[4].source)
        self.assertEqual('/some/source/cover.jpg', commands[5].source)
