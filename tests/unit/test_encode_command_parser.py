import mock
import unittest
from amu.clidriver import CliDriver
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command
from amu.parsing import CommandParsingError
from amu.parsing import EncodeCommandParser

class EncodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_and_destination_are_files__returns_single_encode_wav_to_mp3_command(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = True
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        command = parser.parse_wav_to_mp3('/some/path/to/song.wav', '/some/path/to/song.mp3')
        self.assertIsInstance(command, EncodeWavToMp3Command)
        self.assertEqual('/some/path/to/song.wav', command.source)
        self.assertEqual('/some/path/to/song.mp3', command.destination)

    @mock.patch('os.path.exists')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_does_not_exist__throws_command_parsing_exception(self, config_mock, cd_ripper_mock, encoder_mock, exists_mock):
        exists_mock.return_value = False
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory or wav file must exist'):
            parser.parse_wav_to_mp3('/some/path/to/song.wav', '/some/path/to/song.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_is_directory_with_4_wav_files__returns_4_correctly_specified_encode_wav_to_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_is_multi_cd_release__returns_8_correctly_specified_encode_wav_to_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', ('cd1', 'cd2'), ()),
            ('/some/path/to/wavs/cd1', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav')),
            ('/some/path/to/wavs/cd2', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(8, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/cd1/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/cd1/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/cd1/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/cd1/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.mp3')
        self.assertEqual(commands[4].source, '/some/path/to/wavs/cd2/01 - Track 1.wav')
        self.assertEqual(commands[4].destination, '/some/destination/cd2/01 - Track 1.mp3')
        self.assertEqual(commands[5].source, '/some/path/to/wavs/cd2/02 - Track 2.wav')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/02 - Track 2.mp3')
        self.assertEqual(commands[6].source, '/some/path/to/wavs/cd2/03 - Track 3.wav')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/03 - Track 3.mp3')
        self.assertEqual(commands[7].source, '/some/path/to/wavs/cd2/04 - Track 4.wav')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/04 - Track 4.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_contains_files_that_are_not_wavs__commands_should_not_be_generated_for_non_wav_files(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', 'rip.log', 'description.txt'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))
