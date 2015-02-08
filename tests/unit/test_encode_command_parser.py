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
