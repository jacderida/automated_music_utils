import mock
import subprocess
import unittest
from mock import MagicMock
from amu.config import ConfigurationError
from amu.encode import LameEncoder


class LameEncoderTest(unittest.TestCase):
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    @mock.patch('amu.encode.os.path.isdir')
    @mock.patch('amu.encode.os.path.exists')
    def test__encode_wav_to_mp3__lame_is_used_as_encoder__lame_is_called_with_the_correct_args(self, exists_mock, isdir_mock, subprocess_mock, config_mock, open_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = False
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_encoding_setting.return_value = '-V0'
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

    @mock.patch('amu.encode.os.path.exists')
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    def test__encode_wav_to_mp3__source_is_non_existent__throws_configuration_exception(self, config_mock, exists_mock):
        exists_mock.return_value = False
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_encoding_setting.return_value = '-V0'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        with self.assertRaisesRegexp(ConfigurationError, 'The source to encode does not exist'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav_to_mp3('/some/path/source', '/some/path/destination')

    @mock.patch('amu.encode.os.path.exists')
    @mock.patch('amu.encode.os.path.isdir')
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    def test__encode_wav_to_mp3__source_is_directory__throws_configuration_exception(self, config_mock, isdir_mock, exists_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = True
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_encoding_setting.return_value = '-V0'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        with self.assertRaisesRegexp(ConfigurationError, 'The source should not be a directory'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav_to_mp3('/some/path/source', '/some/path/destination')
