import mock
import unittest
from mock import patch
from amu.config import ConfigurationError
from amu.config import ConfigurationProvider


class ConfigurationProviderTest(unittest.TestCase):
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_on_path__returns_ruby_ripper_command(self):
        config_provider = ConfigurationProvider()
        with patch('amu.rip.subprocess.call') as mock:
            mock.return_value = 0
            result = config_provider.get_ruby_ripper_path()
            self.assertEqual('rubyripper_cli', result)
            mock.assert_called_with(['which', 'rubyripper_cli'])

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
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

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__environment_variable_has_incorrect_path__throws_configuration_error(self, subprocess_mock, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = \
            '/opt/rubyripper/rubyripper_cli.rb'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock, config_get_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        result = config_provider.get_ruby_ripper_path()
        self.assertEqual('/opt/rubyripper/rubyripper_cli.rb', result)
        config_get_mock.assert_called_with('ripper', 'path')

    @mock.patch('amu.rip.ConfigParser.ConfigParser.read')
    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.path.expanduser')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        config_provider.get_ruby_ripper_path()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.path.expanduser')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__invalid_config_file__throws_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.rip.ConfigParser.ConfigParser.read')
    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.path.expanduser')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__config_file_specifies_incorrect_path__throws_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.side_effect = [True, False]
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_path()

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    def test__get_ruby_ripper_config_file__ruby_ripper_config_file_is_set_on_environment_variable__returns_correct_path(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        result = config_provider.get_ruby_ripper_config_file()
        self.assertEqual('/home/user/ripper_config_file', result)

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    def test__get_ruby_ripper_config_file__ruby_ripper_config_file_is_set_on_environment_variable__correct_variable_used(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider.get_ruby_ripper_config_file()
        environ_mock.get.assert_called_with('RUBYRIPPER_CONFIG_PATH')

    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    def test__get_ruby_ripper_config_file__environment_variable_has_incorrect_path__throws_configuration_error(self, environ_mock, path_exists_mock):
        config_provider = ConfigurationProvider()
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_config_file()

    @mock.patch('amu.rip.ConfigParser.ConfigParser.read')
    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.exists')
    @mock.patch('amu.rip.os.environ')
    def test__get_temp_config_path_for_ripper__temp_path_defined_in_config_file__returned_path_contains_temp_path(self, environ_mock, path_exists_mock, config_get_mock, config_read_mock):
        config_get_mock.return_value = '/tmp'
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider = ConfigurationProvider()
        result = config_provider.get_temp_config_path_for_ripper()
        self.assertIn('/tmp/', result)
