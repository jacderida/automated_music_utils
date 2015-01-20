import mock
import unittest
import uuid
from mock import MagicMock
from mock import patch
from amu.config import ConfigurationError
from amu.config import ConfigurationProvider


class ConfigurationProviderTest(unittest.TestCase):
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_on_path__returns_ruby_ripper_command(self):
        config_provider = ConfigurationProvider()
        with patch('amu.config.subprocess.call') as mock:
            mock.return_value = 0
            result = config_provider.get_ruby_ripper_path()
            self.assertEqual('rubyripper_cli', result)
            mock.assert_called_with(['which', 'rubyripper_cli'])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_path_is_set_on_environment_variable__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = \
            '/opt/rubyripper/rubyripper_cli.rb'
        path_exists_mock.return_value = True
        result = config_provider.get_ruby_ripper_path()
        self.assertEqual(
            '/opt/rubyripper/rubyripper_cli.rb', result)
        environ_mock.get.assert_called_with('RUBYRIPPER_CLI_PATH')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__environment_variable_has_incorrect_path__throws_configuration_error(self, subprocess_mock, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = \
            '/opt/rubyripper/rubyripper_cli.rb'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock, config_get_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        result = config_provider.get_ruby_ripper_path()
        self.assertEqual('/opt/rubyripper/rubyripper_cli.rb', result)
        config_get_mock.assert_called_with('ripper', 'path')

    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        config_provider.get_ruby_ripper_path()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__invalid_config_file__throws_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__config_file_specifies_incorrect_path__throws_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.side_effect = [True, False]
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_ruby_ripper_config_file__ruby_ripper_config_file_is_set_on_environment_variable__returns_correct_path(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        result = config_provider.get_ruby_ripper_config_file()
        self.assertEqual('/home/user/ripper_config_file', result)

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_ruby_ripper_config_file__ruby_ripper_config_file_is_set_on_environment_variable__correct_variable_used(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider.get_ruby_ripper_config_file()
        environ_mock.get.assert_called_with('RUBYRIPPER_CONFIG_PATH')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_ruby_ripper_config_file__environment_variable_has_incorrect_path__throws_configuration_error(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_config_file()

    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__temp_path_defined_in_config_file__returned_path_contains_temp_path(self, environ_mock, path_exists_mock, config_get_mock, open_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_get_mock.return_value = '/tmp'
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider = ConfigurationProvider()
        result = config_provider.get_temp_config_file_for_ripper()
        self.assertIn('/tmp/', result)

    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__guid_used_for_file_name__returned_path_file_name_is_guid(self, environ_mock, path_exists_mock, config_get_mock, open_mock):
        open_mock.return_value = MagicMock(spec=file)
        config_get_mock.return_value = '/tmp'
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider = ConfigurationProvider()
        result = config_provider.get_temp_config_file_for_ripper()
        parsed_uuid = result.split('/tmp/')[1]
        # Seems a reasonable assertion; UUID will throw if string is not valid.
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    @mock.patch('amu.config.re.sub')
    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__replace_output_destination_in_temp_config_file__destination_is_replaced(self, environ_mock, path_exists_mock, config_get_mock, open_mock, sub_mock):
        sample_file_contents = [
            'mp3=false',
            'cdrom=/dev/cdrom',
            'basedir=REPLACE_BASE_DIR'
        ]
        open_mock.return_value = MagicMock(spec=file)
        config_get_mock.return_value = '/tmp'
        file_handle = open_mock.return_value.__enter__.return_value
        file_handle.readlines.return_value = sample_file_contents
        config_provider = ConfigurationProvider()
        config_provider.get_temp_config_file_for_ripper()
        sub_mock.assert_called_with('REPLACE_BASE_DIR', AnyStringWith('/tmp/'), 'basedir=REPLACE_BASE_DIR')

class AnyStringWith(str):
    def __eq__(self, other):
        return self in other
