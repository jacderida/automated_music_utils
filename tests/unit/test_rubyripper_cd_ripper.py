import unittest
from mock import Mock
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

    def test_is_installed_ruby_ripper_path_is_set_on_environment_variable_correctly_set(self):
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
