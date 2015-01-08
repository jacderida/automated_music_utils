import mock
import os
import unittest
from mock import patch
from amu.rip import RubyRipperCdRipper


class RubyRipperCdRipperTest(unittest.TestCase):
    def test_is_installed_ruby_ripper_cli_is_on_path_ripper_path_correctly_set(self):
        ripper = RubyRipperCdRipper()
        with patch('amu.rip.subprocess.call') as mock:
            mock.return_value = 0
            result = ripper.is_installed()
            self.assertTrue(result)
            self.assertEqual('rubyripper_cli', ripper.rubyripper_path)
            mock.assert_called_with(['which', 'rubyripper_cli'])

    def test_is_installed_ruby_ripper_path_is_set_on_environment_variable_ripper_path_correctly_set(self):
        ripper = RubyRipperCdRipper()
        with patch('amu.rip.subprocess.call') as subprocess_mock:
            with patch('amu.rip.os.environ') as environ_mock:
                subprocess_mock.return_value = 1
                environ_mock.get.return_value = \
                    '/opt/rubyripper/rubyripper_cli.rb'
                result = ripper.is_installed()
                self.assertTrue(result)
                self.assertEqual(
                    '/opt/rubyripper/rubyripper_cli.rb', ripper.rubyripper_path)
                environ_mock.get.assert_called_with('RUBYRIPPER_CLI_PATH')

    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test_is_installed_ruby_ripper_cli_is_in_config_file_ripper_path_correctly_set(self, subprocess_mock, environ_mock, config_get_mock):
        ripper = RubyRipperCdRipper()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        result = ripper.is_installed()
        self.assertTrue(result)
        self.assertEqual(
            '/opt/rubyripper/rubyripper_cli.rb',
            ripper.rubyripper_path)
        config_get_mock.assert_called_with('ripper', 'path')

    @mock.patch('amu.rip.ConfigParser.ConfigParser.read')
    @mock.patch('amu.rip.ConfigParser.ConfigParser.get')
    @mock.patch('amu.rip.os.path.expanduser')
    @mock.patch('amu.rip.os.environ')
    @mock.patch('amu.rip.subprocess.call')
    def test_is_installed_ruby_ripper_cli_is_in_config_file_correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, config_get_mock, config_read_mock):
        ripper = RubyRipperCdRipper()
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        config_get_mock.return_value = '/opt/rubyripper/rubyripper_cli.rb'
        result = ripper.is_installed()
        self.assertTrue(result)
        config_read_mock.assert_called_with('/home/user/.amu_config')
