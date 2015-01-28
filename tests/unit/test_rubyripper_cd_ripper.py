import mock
import subprocess
import unittest
import uuid
from mock import call, MagicMock
from amu import utils
from amu.config import ConfigurationError
from amu.rip import RubyRipperCdRipper


class RubyRipperCdRipperTest(unittest.TestCase):
    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__call_ruby_ripper_with_correct_args__ruby_ripper_is_called_with_correct_args(self, subprocess_mock, config_mock, open_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        path_exists_mock.return_value = True
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

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__temporary_directory_has_guid__temp_directory_created_with_guid(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        path_exists_mock.return_value = True
        stored_args_mock = utils.get_mock_with_stored_call_args(config_mock)
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(stored_args_mock)
        ripper.rip_cd('/some/path')
        temp_path = stored_args_mock.get_temp_config_file_for_ripper.call_args[0][0]
        parsed_uuid = temp_path.split('/tmp/')[1]
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__the_os_should_be_used_to_get_temp_dir__os_temp_dir_is_used(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        path_exists_mock.return_value = True
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

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__ripper_should_use_temp_directory_as_destination__temp_directory_is_destination(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        stored_args_mock = utils.get_mock_with_stored_call_args(config_mock)
        path_exists_mock.return_value = True
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(stored_args_mock)
        ripper.rip_cd('/some/path')
        temp_path = stored_args_mock.get_temp_config_file_for_ripper.call_args[0][0]
        stored_args_mock.get_temp_config_file_for_ripper.assert_called_once_with(temp_path)

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__temp_output_should_be_copied_to_destination__temp_output_is_copied_to_destination(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        stored_args_mock = utils.get_mock_with_stored_call_args(config_mock)
        path_exists_mock.return_value = True
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(stored_args_mock)
        ripper.rip_cd('/some/path')
        temp_path = stored_args_mock.get_temp_config_file_for_ripper.call_args[0][0]
        copy_content_mock.assert_called_once_with(temp_path, '/some/path')

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__temp_directory_should_be_removed__temp_directory_is_removed(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        stored_args_mock = utils.get_mock_with_stored_call_args(config_mock)
        path_exists_mock.return_value = True
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(stored_args_mock)
        ripper.rip_cd('/some/path')
        temp_path = stored_args_mock.get_temp_config_file_for_ripper.call_args[0][0]
        rm_mock.assert_called_once_with(temp_path)

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.mkdir')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__destination_does_not_exist__destination_should_be_created(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, mkdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        path_exists_mock.return_value = False
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
        mkdir_mock.assert_called_once_with('/some/path')

    @mock.patch('amu.rip.os.remove')
    @mock.patch('amu.rip.shutil.rmtree')
    @mock.patch('amu.rip.utils.copy_content_to_directory')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__temp_config_file_should_be_removed__temp_config_file_is_removed(self, subprocess_mock, config_mock, open_mock, gettempdir_mock, path_exists_mock, copy_content_mock, rm_mock, remove_mock):
        path_exists_mock.return_value = True
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
        remove_mock.assert_called_once_with('/opt/rubyripper/config_file')

    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    def test__rip_cd__empty_destination__throws_configuration_exception(self, config_mock):
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_temp_config_file_for_ripper.return_value = \
            '/opt/rubyripper/config_file'
        with self.assertRaises(ConfigurationError):
            ripper = RubyRipperCdRipper(config_mock)
            ripper.rip_cd('')
