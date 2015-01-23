import mock
import subprocess
import unittest
import uuid
from copy import deepcopy
from mock import DEFAULT, MagicMock, Mock, patch
from amu.rip import RubyRipperCdRipper


class RubyRipperCdRipperTest(unittest.TestCase):
    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__call_ruby_ripper_with_correct_args__ruby_ripper_is_called_with_correct_args(self, subprocess_mock, config_mock, open_mock, mkdir_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(config_mock)
        ripper.rip_cd('/some/path')
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
        ripper.rip_cd('/some/path')
        mkdir_mock.assert_called_with(AnyStringWith('/tmp/'))

    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__temporary_directory_has_guid__temp_directory_created_with_guid(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, mkdir_mock):
        copy_mock = self.copy_call_args(mkdir_mock)
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
        ripper.rip_cd('/some/path')
        temp_path = copy_mock.call_args[0][0]
        parsed_uuid = temp_path.split('/tmp/')[1]
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__the_os_should_be_used_to_get_temp_dir__os_temp_dir_is_used(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, mkdir_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(config_mock)
        ripper.rip_cd('/some/path')
        gettempdir_mock.assert_called_once_with()

    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__ripper_should_use_temp_directory_as_destination__temp_directory_is_destination(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, mkdir_mock):
        copy_mock = self.copy_call_args(mkdir_mock)
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
        ripper.rip_cd('/some/path')
        temp_path = copy_mock.call_args[0][0]
        config_mock.get_temp_config_file_for_ripper.assert_called_once_with(temp_path)

    def copy_call_args(self, mock):
        new_mock = Mock()
        def side_effect(*args, **kwargs):
            args = deepcopy(args)
            kwargs = deepcopy(kwargs)
            new_mock(*args, **kwargs)
            return DEFAULT
        mock.side_effect = side_effect
        return new_mock

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other
