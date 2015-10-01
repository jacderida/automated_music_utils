import mock
import unittest
from mock import Mock
from amu.commands import DecodeAudioCommand
from amu.parsing import CommandParsingError
from amu.parsing import DecodeCommandParser


class DecodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_file__returns_single_decode_flac_command(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertIsInstance(command, DecodeAudioCommand)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_file__source_is_specified_correctly(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertEqual('/some/source.flac', command.source)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_file__destination_is_specified_correctly(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertEqual('/some/destination.wav', command.destination)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_does_not_exist__raises_command_parsing_error(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = False
        config_mock, encoder_mock = (Mock(),)*2
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory or file must exist'):
            parser = DecodeCommandParser(config_mock, encoder_mock)
            parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_directory_with_4_flac_files__returns_4_correctly_specified_decode_audio_file_commands(self, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/flacs', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac'))
        ]
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        commands = parser.parse_decode_flac_command('/some/path/to/flacs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/flacs/01 - Track 1.flac')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].source, '/some/path/to/flacs/02 - Track 2.flac')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.wav')
        self.assertEqual(commands[2].source, '/some/path/to/flacs/03 - Track 3.flac')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.wav')
        self.assertEqual(commands[3].source, '/some/path/to/flacs/04 - Track 4.flac')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.wav')
