import mock
import unittest
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command

class EncodeWavToMp3CommandTest(unittest.TestCase):
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__execute__encoder_called_correctly__is_called_with_correct_source(self, config_mock, encoder_mock):
        command = EncodeWavToMp3Command(config_mock, encoder_mock)
        command.source = '/some/source'
        command.destination = '/some/destination'
        command.execute()
        encoder_mock.encode_wav_to_mp3.assert_called_once_with('/some/source', '/some/destination')
