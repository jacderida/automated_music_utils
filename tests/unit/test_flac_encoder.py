import mock
import subprocess
import unittest
from mock import MagicMock, Mock
from amu.audio import FlacEncoder
from amu.config import ConfigurationError


class FlacEncoderTest(unittest.TestCase):
    @mock.patch('amu.audio.open', create=True)
    @mock.patch('subprocess.Popen')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    def test__encode_wav__flac_is_used_as_encoder__flac_is_called_with_the_correct_args(self, exists_mock, isdir_mock, subprocess_mock, open_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = False
        open_mock.return_value = MagicMock(spec=file)
        config_mock = Mock(autospec=True)
        config_mock.get_lame_path.return_value = '/opt/flac/flac'
        config_mock.get_lame_encoding_setting.return_value = '-8'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        encoder = FlacEncoder(config_mock)
        encoder.encode_wav('/some/path/source', '/some/path/destination')
        subprocess_args = [
            '/opt/flac/flac',
            '-8',
            '/some/path/source',
            '/some/path/destination'
        ]
        subprocess_mock.assert_called_with(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
