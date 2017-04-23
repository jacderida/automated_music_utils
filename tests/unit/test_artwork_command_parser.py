import mock
import unittest
from mock import Mock
from amu.commands import AddArtworkCommand
from amu.commands import EncodeWavCommand
from amu.parsing import ArtworkCommandParser
from amu.parsing import CommandParsingError

class ArtworkCommandParserTest(unittest.TestCase):
    def test__parse_add_artwork_command__source_is_file__an_add_artwork_command_should_be_returned(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
        self.assertIsInstance(commands[0], AddArtworkCommand)

    def test__parse_add_artwork_command__source_is_file__add_artwork_command_should_have_source_specified_correctly(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
        self.assertEqual(source, commands[0].source)

    def test__parse_add_artwork_command__source_is_file__add_artwork_command_should_have_destination_specified_correctly(self):
        source = '/some/source/artwork.jpg'
        destination = '/some/destination/audio.mp3'
        config_mock, tagger_mock = (Mock(),)*2
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
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
            parser.parse_add_artwork_command(source, destination, 'mp3')

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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
        self.assertEqual(3, len(commands))

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_directory_and_format_is_flac__returns_3_add_artwork_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/source'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [('/some/source', (), ('01 - Track 01.flac', '02 - Track 02.flac', '03 - Track 03.flac'))]
        listdir_mock.side_effect = [['01 - Track 01.flac', '02 - Track 02.flac', '03 - Track 03.flac', 'cover.jpg']]
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination, 'flac')
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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
        self.assertEqual('/some/source/cd1/01 - Track 01.mp3', commands[0].destination)
        self.assertEqual('/some/source/cd1/02 - Track 02.mp3', commands[1].destination)
        self.assertEqual('/some/source/cd1/03 - Track 03.mp3', commands[2].destination)
        self.assertEqual('/some/source/cd2/01 - Track 01.mp3', commands[3].destination)
        self.assertEqual('/some/source/cd2/02 - Track 02.mp3', commands[4].destination)
        self.assertEqual('/some/source/cd2/03 - Track 03.mp3', commands[5].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_add_artwork_command__destination_is_multi_cd_and_format_is_flac__destination_should_be_set_correctly_on_commands(self, walk_mock, listdir_mock, isdir_mock):
        source = '/some/source'
        destination = '/some/destination'
        config_mock, tagger_mock = (Mock(),)*2
        isdir_mock.side_effect = [True, True]
        walk_mock.return_value = [
            ('/some/source', ('cd1', 'cd2'), ()),
            ('/some/source/cd1', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac')),
            ('/some/source/cd2', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 01.flac', '02 - Track 02.flac', '03 - Track 03.flac', 'cover.jpg'],
            ['01 - Track 01.flac', '02 - Track 02.flac', '03 - Track 03.flac'],
            ['01 - Track 01.flac', '02 - Track 02.flac', '03 - Track 03.flac']
        ]
        parser = ArtworkCommandParser(config_mock, tagger_mock)
        commands = parser.parse_add_artwork_command(source, destination, 'flac')
        self.assertEqual(6, len(commands))

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
        commands = parser.parse_add_artwork_command(source, destination, 'mp3')
        self.assertEqual('/some/source/cover.jpg', commands[0].source)
        self.assertEqual('/some/source/cover.jpg', commands[1].source)
        self.assertEqual('/some/source/cover.jpg', commands[2].source)
        self.assertEqual('/some/source/cover.jpg', commands[3].source)
        self.assertEqual('/some/source/cover.jpg', commands[4].source)
        self.assertEqual('/some/source/cover.jpg', commands[5].source)

    @mock.patch('os.listdir')
    def test__parse_from_encode_commands__4_encode_commands_and_source_has_cover_jpg__returns_4_add_artwork_commands(self, listdir_mock):
        config_mock, tagger_mock, encoder_mock = (Mock(),)*3
        listdir_mock.return_value = [
            '01 - Track 01.wav', '02 - Track 02.wav', '03 - Track 03.wav', '04 - Track 04.wav', 'cover.jpg'
        ]
        commands = []
        command1 = EncodeWavCommand(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavCommand(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavCommand(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavCommand(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

        parser = ArtworkCommandParser(config_mock, tagger_mock)
        artwork_commands = parser.parse_from_encode_commands(commands)
        self.assertEqual(4, len(artwork_commands))
        self.assertIsInstance(artwork_commands[0], AddArtworkCommand)
        self.assertIsInstance(artwork_commands[1], AddArtworkCommand)
        self.assertIsInstance(artwork_commands[2], AddArtworkCommand)
        self.assertIsInstance(artwork_commands[3], AddArtworkCommand)

    @mock.patch('os.listdir')
    def test__parse_from_encode_commands__4_encode_commands_and_source_has_cover_jpg__commands_have_source_specified_correctly(self, listdir_mock):
        config_mock, tagger_mock, encoder_mock = (Mock(),)*3
        listdir_mock.return_value = [
            '01 - Track 01.wav', '02 - Track 02.wav', '03 - Track 03.wav', '04 - Track 04.wav', 'cover.jpg'
        ]
        commands = []
        command1 = EncodeWavCommand(config_mock, encoder_mock)
        command1.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavCommand(config_mock, encoder_mock)
        command2.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavCommand(config_mock, encoder_mock)
        command3.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavCommand(config_mock, encoder_mock)
        command4.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

        parser = ArtworkCommandParser(config_mock, tagger_mock)
        artwork_commands = parser.parse_from_encode_commands(commands)
        self.assertEqual(artwork_commands[0].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.jpg')
        self.assertEqual(artwork_commands[1].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.jpg')
        self.assertEqual(artwork_commands[2].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.jpg')
        self.assertEqual(artwork_commands[3].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.jpg')

    @mock.patch('os.listdir')
    def test__parse_from_encode_commands__4_encode_commands_and_source_has_cover_png__commands_have_source_specified_correctly(self, listdir_mock):
        config_mock, tagger_mock, encoder_mock = (Mock(),)*3
        listdir_mock.return_value = [
            '01 - Track 01.wav', '02 - Track 02.wav', '03 - Track 03.wav', '04 - Track 04.wav', 'cover.png'
        ]
        commands = []
        command1 = EncodeWavCommand(config_mock, encoder_mock)
        command1.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavCommand(config_mock, encoder_mock)
        command2.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavCommand(config_mock, encoder_mock)
        command3.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavCommand(config_mock, encoder_mock)
        command4.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

        parser = ArtworkCommandParser(config_mock, tagger_mock)
        artwork_commands = parser.parse_from_encode_commands(commands)
        self.assertEqual(artwork_commands[0].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.png')
        self.assertEqual(artwork_commands[1].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.png')
        self.assertEqual(artwork_commands[2].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.png')
        self.assertEqual(artwork_commands[3].source, '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/cover.png')

    @mock.patch('os.listdir')
    def test__parse_from_encode_commands__4_encode_commands_and_source_has_cover_jpg__commands_have_destination_specified_correctly(self, listdir_mock):
        config_mock, tagger_mock, encoder_mock = (Mock(),)*3
        listdir_mock.return_value = [
            '01 - Track 01.wav', '02 - Track 02.wav', '03 - Track 03.wav', '04 - Track 04.wav', 'cover.jpg'
        ]
        commands = []
        command1 = EncodeWavCommand(config_mock, encoder_mock)
        command1.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavCommand(config_mock, encoder_mock)
        command2.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavCommand(config_mock, encoder_mock)
        command3.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavCommand(config_mock, encoder_mock)
        command4.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

        parser = ArtworkCommandParser(config_mock, tagger_mock)
        artwork_commands = parser.parse_from_encode_commands(commands)
        self.assertEqual(artwork_commands[0].destination, '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3')
        self.assertEqual(artwork_commands[1].destination, '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3')
        self.assertEqual(artwork_commands[2].destination, '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3')
        self.assertEqual(artwork_commands[3].destination, '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3')

    @mock.patch('os.listdir')
    def test__parse_from_encode_commands__4_encode_commands_source_has_no_cover__returns_empty_list(self, listdir_mock):
        config_mock, tagger_mock, encoder_mock = (Mock(),)*3
        listdir_mock.return_value = [
            '01 - Track 01.wav', '02 - Track 02.wav', '03 - Track 03.wav', '04 - Track 04.wav'
        ]
        commands = []
        command1 = EncodeWavCommand(config_mock, encoder_mock)
        command1.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavCommand(config_mock, encoder_mock)
        command2.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavCommand(config_mock, encoder_mock)
        command3.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavCommand(config_mock, encoder_mock)
        command4.source = '/wav/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/mp3/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

        parser = ArtworkCommandParser(config_mock, tagger_mock)
        artwork_commands = parser.parse_from_encode_commands(commands)
        self.assertEqual(0, len(artwork_commands))
