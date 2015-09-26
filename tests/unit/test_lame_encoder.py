import mock
import subprocess
import unittest
from mock import MagicMock, Mock
from amu.audio import LameEncoder
from amu.config import ConfigurationError


class LameEncoderTest(unittest.TestCase):
    @mock.patch('amu.audio.open', create=True)
    @mock.patch('subprocess.Popen')
    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    def test__encode_wav__lame_is_used_as_encoder__lame_is_called_with_the_correct_args(self, exists_mock, isdir_mock, subprocess_mock, open_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = False
        open_mock.return_value = MagicMock(spec=file)
        config_mock = Mock(autospec=True)
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_lame_encoding_setting.return_value = '-V0'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        encoder = LameEncoder(config_mock)
        encoder.encode_wav('/some/path/source', '/some/path/destination')
        subprocess_args = [
            '/opt/lame/lame',
            '-V0',
            '/some/path/source',
            '/some/path/destination'
        ]
        subprocess_mock.assert_called_with(subprocess_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def test__encode_wav__source_is_empty__raises_value_error(self):
        config_mock = Mock(autospec=True)
        with self.assertRaisesRegexp(ValueError, 'A value must be supplied for the source'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav('', '/some/path/destination')

    def test__encode_wav__destination_is_empty__raises_value_error(self):
        config_mock = Mock(autospec=True)
        with self.assertRaisesRegexp(ValueError, 'A value must be supplied for the destination'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav('/some/path/source', '')

    @mock.patch('os.path.exists')
    def test__encode_wav__source_is_non_existent__throws_configuration_exception(self, exists_mock):
        exists_mock.return_value = False
        config_mock = Mock(autospec=True)
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_lame_encoding_setting.return_value = '-V0'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        with self.assertRaisesRegexp(ConfigurationError, 'The source to encode does not exist'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav('/some/path/source', '/some/path/destination')

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isdir')
    def test__encode_wav__source_is_directory__throws_configuration_exception(self, isdir_mock, exists_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = True
        config_mock = Mock(autospec=True)
        config_mock.get_lame_path.return_value = '/opt/lame/lame'
        config_mock.get_lame_encoding_setting.return_value = '-V0'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        with self.assertRaisesRegexp(ConfigurationError, 'The source should not be a directory'):
            encoder = LameEncoder(config_mock)
            encoder.encode_wav('/some/path/source', '/some/path/destination')
