import mock
import subprocess
import unittest
from mock import MagicMock
from amu.encode import LameEncoder


class LameEncoderTest(unittest.TestCase):
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__encode_wav_to_mp3__lame_is_used_as_encoder__lame_is_called_with_the_correct_args(self, subprocess_mock, config_mock, open_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        encoder = LameEncoder(config_mock)
        encoder.encode_wav_to_mp3('/some/path/source', '/some/path/destination')
        subprocess_args = [
            '/opt/lame/lame',
            '-V0',
            '/some/path/source',
            '/some/path/destination'
        ]
        subprocess_mock.assert_called_with(subprocess_args, stdout=subprocess.PIPE)
