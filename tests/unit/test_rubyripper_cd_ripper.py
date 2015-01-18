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
        config_mock.get_ruby_ripper_config_file.return_value = \
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

    @mock.patch('amu.rip.re.sub')
    @mock.patch('amu.rip.open', create=True)
    @mock.patch('amu.rip.ConfigurationProvider', autospec=True)
    @mock.patch('amu.rip.subprocess.Popen')
    def test__rip_cd__replace_output_destination_in_config_file__destination_is_replaced_in_config_file(self, subprocess_mock, config_mock, open_mock, sub_mock):
        sample_file_contents = [
            'mp3=false',
            'cdrom=/dev/cdrom',
            'basedir=REPLACE_BASE_DIR'
        ]
        open_mock.return_value = MagicMock(spec=file)
        file_handle = open_mock.return_value.__enter__.return_value
        file_handle.readlines.return_value = sample_file_contents
        config_mock.get_ruby_ripper_path.return_value = \
            '/opt/rubyripper/rubyripper_cli'
        config_mock.get_ruby_ripper_config_file.return_value = \
            '/opt/rubyripper/config_file'
        process_mock = mock.Mock()
        process_mock.stdout.readline = lambda: ""
        subprocess_mock.return_value = process_mock
        ripper = RubyRipperCdRipper(config_mock)
        ripper.rip_cd()
        sub_mock.assert_called_with('REPLACE_BASE_DIR', '/tmp/rip', 'basedir=REPLACE_BASE_DIR')
