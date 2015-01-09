import mock
import unittest
from mock import patch
from amu.config import ConfigurationProvider


class ConfigurationProviderTest(unittest.TestCase):
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_on_path__returns_ruby_ripper_command(self):
        config_provider = ConfigurationProvider()
        with patch('amu.rip.subprocess.call') as mock:
            mock.return_value = 0
            result = config_provider.get_ruby_ripper_path()
            self.assertEqual('rubyripper_cli', result)
            mock.assert_called_with(['which', 'rubyripper_cli'])

    def test__get_ruby_ripper_path__ruby_ripper_path_is_set_on_environment_variable__returns_correct_path(self):
        config_provider = ConfigurationProvider()
        with patch('amu.rip.subprocess.call') as subprocess_mock:
            with patch('amu.rip.os.environ') as environ_mock:
                subprocess_mock.return_value = 1
                environ_mock.get.return_value = \
                    '/opt/rubyripper/rubyripper_cli.rb'
                result = config_provider.get_ruby_ripper_path()
                self.assertEqual(
                    '/opt/rubyripper/rubyripper_cli.rb', result)
                environ_mock.get.assert_called_with('RUBYRIPPER_CLI_PATH')

    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__returns_correct_path(self, subprocess_mock, environ_mock, config_get_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        result = config_provider.get_ruby_ripper_path()
        self.assertEqual('/opt/rubyripper/rubyripper_cli.rb', result)
        config_get_mock.assert_called_with('ripper', 'path')

    @mock.patch('amu.rip.ConfigParser.ConfigParser.read')
    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.expanduser')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_in_config_file__correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, config_get_mock, config_read_mock):
        config_provider = ConfigurationProvider()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        config_provider.get_ruby_ripper_path()
        config_read_mock.assert_called_with('/home/user/.amu_config')
