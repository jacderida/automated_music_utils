import mock
import subprocess
import unittest
from mock import MagicMock
from amu.rip import RubyRipperCdRipper


class RubyRipperCdRipperTest(unittest.TestCase):
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__call_ruby_ripper_with_correct_args__ruby_ripper_is_called_with_correct_args(self, subprocess_mock, config_mock, open_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(config_mock)
        ripper.rip_cd()
        subprocess_args = [
            '/opt/rubyripper/rubyripper_cli',
            '--defaults',
            '--file',
            '/opt/rubyripper/config_file'
        ]
        subprocess_mock.assert_called_with(subprocess_args, stdout=subprocess.PIPE)

    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__create_temp_directory_for_output__temp_directory_is_created(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, mkdir_mock):
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(config_mock)
        ripper.rip_cd()
        mkdir_mock.assert_called_with(AnyStringWith('/tmp/'))

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other
