import mock
import unittest
from mock import Mock
from amu.commands import DecodeAudioCommand
from amu.parsing import DecodeCommandParser


class DecodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_file__returns_single_decode_flac_command(self, isfile_mock):
        isfile_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertIsInstance(command, DecodeAudioCommand)

    @mock.patch('os.path.isfile')
    def test__parse_decode_flac_command__source_is_file__source_is_specified_correctly(self, isfile_mock):
        isfile_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        parser = DecodeCommandParser(config_mock, encoder_mock)
        command = parser.parse_decode_flac_command('/some/source.flac', '/some/destination.wav')[0]
        self.assertEqual('/some/source.flac', command.source)
