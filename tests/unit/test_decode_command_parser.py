import mock
import unittest
from mock import Mock
from amu.commands import DecodeAudioCommand
from amu.parsing import CommandParsingError
from amu.parsing import DecodeCommandParser


class DecodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_file__returns_single_decode_flac_command(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertIsInstance(command, DecodeAudioCommand)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_file__source_is_specified_correctly(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertEqual('/some/source.flac', command.source)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_file__destination_is_specified_correctly(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertEqual('/some/destination.wav', command.destination)

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_does_not_exist__raises_command_parsing_error(self, isfile_mock, exists_mock):
        isfile_mock.return_value = True
        exists_mock.return_value = False
        config_mock, encoder_mock = (Mock(),)*2
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory or file must exist'):
            parser = DecodeCommandParser(config_mock, encoder_mock)
            parser.parse_decode_command('/some/source.flac', '/some/destination.wav')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_directory_with_4_flac_files__returns_4_correctly_specified_decode_audio_file_commands(self, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/flacs', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac'))
        ]
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        commands = parser.parse_decode_command('/some/path/to/flacs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/flacs/01 - Track 1.flac')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].source, '/some/path/to/flacs/02 - Track 2.flac')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.wav')
        self.assertEqual(commands[2].source, '/some/path/to/flacs/03 - Track 3.flac')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.wav')
        self.assertEqual(commands[3].source, '/some/path/to/flacs/04 - Track 4.flac')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.wav')

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_multi_cd_release__returns_9_correctly_specified_decode_audio_file_commands(self, isfile_mock, exists_mock, walk_mock, listdir_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/flacs', ('cd1', 'cd2'), ()),
            ('/some/path/to/flacs/cd1', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac')),
            ('/some/path/to/flacs/cd2', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac'],
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac']
        ]
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        commands = parser.parse_decode_command('/some/path/to/flacs', '/some/destination/')
        self.assertEqual(9, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/flacs/cd1/01 - Track 1.flac')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.wav')
        self.assertEqual(commands[1].source, '/some/path/to/flacs/cd1/02 - Track 2.flac')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.wav')
        self.assertEqual(commands[2].source, '/some/path/to/flacs/cd1/03 - Track 3.flac')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.wav')
        self.assertEqual(commands[3].source, '/some/path/to/flacs/cd1/04 - Track 4.flac')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.wav')
        self.assertEqual(commands[4].source, '/some/path/to/flacs/cd1/05 - Track 5.flac')
        self.assertEqual(commands[4].destination, '/some/destination/cd1/05 - Track 5.wav')
        self.assertEqual(commands[5].source, '/some/path/to/flacs/cd2/01 - Track 1.flac')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/01 - Track 1.wav')
        self.assertEqual(commands[6].source, '/some/path/to/flacs/cd2/02 - Track 2.flac')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/02 - Track 2.wav')
        self.assertEqual(commands[7].source, '/some/path/to/flacs/cd2/03 - Track 3.flac')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/03 - Track 3.wav')
        self.assertEqual(commands[8].source, '/some/path/to/flacs/cd2/04 - Track 4.flac')

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_decode_command__source_is_multi_cd_release_and_walk_returns_directories_and_files_in_arbitrary_order__returns_18_correctly_specified_decode_audio_file_commands(self, isfile_mock, exists_mock, walk_mock, listdir_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/flacs', ('cd4', 'cd1', 'cd3', 'cd2'), ()),
            ('/some/path/to/flacs/cd4', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac')),
            ('/some/path/to/flacs/cd1', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac')),
            ('/some/path/to/flacs/cd3', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac')),
            ('/some/path/to/flacs/cd2', (), ('01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac'],
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac'],
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac', '05 - Track 5.flac'],
            ['01 - Track 1.flac', '02 - Track 2.flac', '03 - Track 3.flac', '04 - Track 4.flac']
        ]
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        commands = parser.parse_decode_command('/some/path/to/flacs', '/some/destination/')
        self.assertEqual(18, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/flacs/cd1/01 - Track 1.flac')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.wav')
        self.assertEqual(commands[1].source, '/some/path/to/flacs/cd1/02 - Track 2.flac')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.wav')
        self.assertEqual(commands[2].source, '/some/path/to/flacs/cd1/03 - Track 3.flac')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.wav')
        self.assertEqual(commands[3].source, '/some/path/to/flacs/cd1/04 - Track 4.flac')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.wav')
        self.assertEqual(commands[4].source, '/some/path/to/flacs/cd1/05 - Track 5.flac')
        self.assertEqual(commands[4].destination, '/some/destination/cd1/05 - Track 5.wav')
        self.assertEqual(commands[5].source, '/some/path/to/flacs/cd2/01 - Track 1.flac')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/01 - Track 1.wav')
        self.assertEqual(commands[6].source, '/some/path/to/flacs/cd2/02 - Track 2.flac')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/02 - Track 2.wav')
        self.assertEqual(commands[7].source, '/some/path/to/flacs/cd2/03 - Track 3.flac')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/03 - Track 3.wav')
        self.assertEqual(commands[8].source, '/some/path/to/flacs/cd2/04 - Track 4.flac')
        self.assertEqual(commands[8].destination, '/some/destination/cd2/04 - Track 4.wav')
        self.assertEqual(commands[9].source, '/some/path/to/flacs/cd3/01 - Track 1.flac')
        self.assertEqual(commands[9].destination, '/some/destination/cd3/01 - Track 1.wav')
        self.assertEqual(commands[10].source, '/some/path/to/flacs/cd3/02 - Track 2.flac')
        self.assertEqual(commands[10].destination, '/some/destination/cd3/02 - Track 2.wav')
        self.assertEqual(commands[11].source, '/some/path/to/flacs/cd3/03 - Track 3.flac')
        self.assertEqual(commands[11].destination, '/some/destination/cd3/03 - Track 3.wav')
        self.assertEqual(commands[12].source, '/some/path/to/flacs/cd3/04 - Track 4.flac')
        self.assertEqual(commands[12].destination, '/some/destination/cd3/04 - Track 4.wav')
        self.assertEqual(commands[13].source, '/some/path/to/flacs/cd3/05 - Track 5.flac')
        self.assertEqual(commands[13].destination, '/some/destination/cd3/05 - Track 5.wav')
        self.assertEqual(commands[14].source, '/some/path/to/flacs/cd4/01 - Track 1.flac')
        self.assertEqual(commands[14].destination, '/some/destination/cd4/01 - Track 1.wav')
        self.assertEqual(commands[15].source, '/some/path/to/flacs/cd4/02 - Track 2.flac')
        self.assertEqual(commands[15].destination, '/some/destination/cd4/02 - Track 2.wav')
        self.assertEqual(commands[16].source, '/some/path/to/flacs/cd4/03 - Track 3.flac')
        self.assertEqual(commands[16].destination, '/some/destination/cd4/03 - Track 3.wav')
        self.assertEqual(commands[17].source, '/some/path/to/flacs/cd4/04 - Track 4.flac')
        self.assertEqual(commands[17].destination, '/some/destination/cd4/04 - Track 4.wav')
