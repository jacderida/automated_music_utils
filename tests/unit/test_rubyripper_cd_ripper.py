import unittest
from mock import Mock
from mock import patch
from amu.rip import RubyRipperCdRipper


class RubyRipperCdRipperTest(unittest.TestCase):
    def test_is_installed_ruby_ripper_cli_is_on_path(self):
        ripper = RubyRipperCdRipper()
        with patch('subprocess.call') as mock:
            mock.return_value = 0
            self.assertTrue(ripper.is_installed())
            self.assertEqual('rubyripper_cli', ripper.rubyripper_path)
