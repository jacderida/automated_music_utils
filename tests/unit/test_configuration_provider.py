import mock
import unittest
import uuid
from mock import MagicMock
from mock import Mock
from mock import patch
from amu import utils
from amu.config import ConfigurationError
from amu.config import ConfigurationProvider
from amu.metadata import MaskReplacer
from amu.models import ReleaseModel


class ConfigurationProviderTest(unittest.TestCase):
    def test__get_ruby_ripper_path__ruby_ripper_cli_is_on_path__returns_ruby_ripper_command(self):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        with patch('amu.config.subprocess.call') as mock:
            mock.return_value = 0
            result = config_provider.get_ruby_ripper_path()
            self.assertEqual('rubyripper_cli', result)
            mock.assert_called_with(['which', 'rubyripper_cli'])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_ruby_ripper_path__ruby_ripper_path_is_set_on_environment_variable__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
    def test__get_ruby_ripper_path__environment_variable_has_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, path_exists_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
    def test__get_ruby_ripper_path__invalid_config_file__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
    def test__get_ruby_ripper_path__config_file_specifies_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
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
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        result = config_provider.get_ruby_ripper_config_file()
        self.assertEqual('/home/user/ripper_config_file', result)

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_ruby_ripper_config_file__ruby_ripper_config_file_is_set_on_environment_variable__correct_variable_used(self, environ_mock, path_exists_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        config_provider.get_ruby_ripper_config_file()
        environ_mock.get.assert_called_with('RUBYRIPPER_CONFIG_PATH')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_ruby_ripper_config_file__environment_variable_has_incorrect_path__raises_configuration_error(self, environ_mock, path_exists_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = False
        with self.assertRaises(ConfigurationError):
            config_provider.get_ruby_ripper_config_file()

    @mock.patch('amu.config.re.sub')
    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__replace_output_destination_in_temp_config_file__destination_is_replaced(self, environ_mock, path_exists_mock, open_mock, sub_mock):
        sample_file_contents = [
            'mp3=false',
            'cdrom=/dev/cdrom',
            'basedir=REPLACE_BASE_DIR'
        ]
        open_mock.return_value = MagicMock(spec=file)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        file_handle = open_mock.return_value.__enter__.return_value
        file_handle.readlines.return_value = sample_file_contents
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_temp_config_file_for_ripper('/any/path')
        sub_mock.assert_called_with('REPLACE_BASE_DIR', '/any/path', 'basedir=REPLACE_BASE_DIR')

    @mock.patch('tempfile.gettempdir')
    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__write_temp_config_file__temp_config_file_is_written(self, environ_mock, path_exists_mock, open_mock, gettempdir_mock):
        open_mock.return_value = MagicMock(spec=file)
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_temp_config_file_for_ripper('/any/path')
        open_mock.assert_called_with(utils.AnyStringWith('/tmp'), 'w')

    @mock.patch('tempfile.gettempdir')
    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__the_os_should_be_used_to_get_temp_dir__os_temp_dir_is_used(self, environ_mock, path_exists_mock, open_mock, gettempdir_mock):
        open_mock.return_value = MagicMock(spec=file)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_temp_config_file_for_ripper('/any/path')
        gettempdir_mock.assert_called_once_with()

    @mock.patch('tempfile.gettempdir')
    @mock.patch('amu.config.open', create=True)
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    def test__get_temp_config_file_for_ripper__the_file_name_should_be_a_guid__the_file_name_is_a_guid(self, environ_mock, path_exists_mock, open_mock, gettempdir_mock):
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        open_mock.return_value = MagicMock(spec=file)
        stored_args_mock = utils.get_mock_with_stored_call_args(open_mock)
        environ_mock.get.return_value = '/home/user/ripper_config_file'
        path_exists_mock.return_value = True
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_temp_config_file_for_ripper('/any/path')
        temp_path = stored_args_mock.call_args[0][0]
        parsed_uuid = temp_path.split('/tmp/')[1]
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    def test__get_temp_config_file_for_ripper__empty_destination_path__raises_configuration_exception(self):
        with self.assertRaises(ConfigurationError):
            directory_selector_mock = Mock()
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_temp_config_file_for_ripper('')

    def test__get_lame_path__lame_is_on_path__lame_returned(self):
        with patch('amu.config.subprocess.call') as mock:
            mock.return_value = 0
            directory_selector_mock = Mock()
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            result = config_provider.get_lame_path()
            self.assertEqual('lame', result)
            mock.assert_called_with(['which', 'lame'])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__lame_path_is_set_on_environment_variable__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = \
            '/some/path/to/lame'
        path_exists_mock.return_value = True
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_lame_path()
        self.assertEqual(
            '/some/path/to/lame', result)
        environ_mock.get.assert_called_with('LAME_PATH')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__environment_variable_has_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = \
            '/some/incorrect/path/to/lame'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaises(ConfigurationError):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_lame_path()

    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__lame_is_in_config_file__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock, config_get_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/some/path/to/lame'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_lame_path()
        self.assertEqual('/some/path/to/lame', result)
        config_get_mock.assert_called_with('encoding', 'lame_path')

    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__lame_is_in_config_file__correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/some/path/to/lame'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_lame_path()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__config_file_does_not_exist__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_lame_path()

    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.os.environ')
    @mock.patch('amu.config.subprocess.call')
    def test__get_lame_path__config_file_specifies_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.side_effect = [True, False]
        config_get_mock.return_value = '/some/path/to/lame'
        directory_selector_mock = Mock()
        with self.assertRaises(ConfigurationError):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_lame_path()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_lame_encoding_setting__encoding_setting_is_in_config_file__returns_correct_value(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = '-V0'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_lame_encoding_setting()
        self.assertEqual('-V0', result)
        config_get_mock.assert_called_with('encoding', 'lame_encoding_setting')

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.get')
    def test__get_lame_encoding_setting__encoding_setting_is_empty__raises_configuration_error(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = ''
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'A value must be provided for the lame encoding setting.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_lame_encoding_setting()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    @mock.patch('amu.config.os.path.expanduser')
    def test__get_lame_encoding_setting__encoding_setting_is_in_config_file__correct_config_file_is_used(self, expanduser_mock, config_get_mock, config_read_mock, path_exists_mock):
        path_exists_mock.return_value = True
        expanduser_mock.return_value = '/home/user/'
        config_get_mock.return_value = '-V0'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_lame_encoding_setting()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    def test__get_lame_encoding_setting__config_file_does_not_exist__raises_configuration_error(self, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_lame_encoding_setting()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_releases_base_directory__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        mask_call = config_get_mock.mock_calls[2]
        self.assertEqual('directories', mask_call[1][0])
        self.assertEqual('mp3_releases_base_directory', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_releases_directories__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        mask_call = config_get_mock.mock_calls[0]
        self.assertEqual('directories', mask_call[1][0])
        self.assertEqual('mp3_release_directories', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__flac_format_is_used__correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'flac')
        mask_call = config_get_mock.mock_calls[0]
        self.assertEqual('directories', mask_call[1][0])
        self.assertEqual('flac_release_directories', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__target_encoding_is_flac__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'flac')
        mask_call = config_get_mock.mock_calls[2]
        self.assertEqual('directories', mask_call[1][0])
        self.assertEqual('flac_releases_base_directory', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_releases_mask__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        mask_call = config_get_mock.mock_calls[1]
        self.assertEqual('masks', mask_call[1][0])
        self.assertEqual('mp3_releases', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__flac_format_is_used__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'flac')
        mask_call = config_get_mock.mock_calls[1]
        self.assertEqual('masks', mask_call[1][0])
        self.assertEqual('flac_releases', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_releases_mask__the_mask_replacer_should_be_used(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        mask_replacer_mock = Mock()
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(mask_replacer_mock, directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        mask_replacer_mock.replace_directory_mask.assert_called_once_with('electronic_directory_mask', release_model)

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_release_base_directory_and_releases_mask__the_correct_destination_should_be_returned(self, config_get_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        self.assertEqual('/path/to/music/Electronic/electronic_directory_mask', result)

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_releases_mask__the_correct_config_file_should_be_read(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '/path/to/music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__releases_base_directory_has_user_home_reference__the_releases_base_directory_should_be_expanded(self, config_get_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.side_effect = ['/home/user/', '/home/user/Music']
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '~/Music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        self.assertEqual('/home/user/Music/Electronic/electronic_directory_mask', result)

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    def test__get_releases_destination_with_mask_replaced__config_file_does_not_exist__raises_configuration_error(self, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__config_file_has_release_directories__it_should_call_the_directory_selector(self, config_get_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.side_effect = ['/home/user/', '/home/user/Music']
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock,Ambient', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '~/Music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')
        directory_selector_mock.select_directory.assert_called_once_with(['Electronic', 'Rock', 'Ambient'])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__release_directories_and_release_masks_are_different_sizes__raises_configuration_error(self, config_get_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.side_effect = ['/home/user/', '/home/user/Music']
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '~/Music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        with self.assertRaisesRegexp(ConfigurationError, 'The release_directories and the mask releases settings must have 2 lists of the same size.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__release_directories_is_empty__raises_configuration_error(self, config_get_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.side_effect = ['/home/user/', '/home/user/Music']
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['', 'electronic_directory_mask@rock_directory_mask@ambient_directory_mask', '~/Music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        with self.assertRaisesRegexp(ConfigurationError, 'The release_directories setting in the amu_config file must have a value.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_releases_destination_with_mask_replaced__release_masks_is_empty__raises_configuration_error(self, config_get_mock, expanduser_mock, path_exists_mock):
        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)

        expanduser_mock.side_effect = ['/home/user/', '/home/user/Music']
        path_exists_mock.return_value = True
        config_get_mock.side_effect = ['Electronic,Rock', '', '~/Music']
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        with self.assertRaisesRegexp(ConfigurationError, 'The masks releases setting in the amu_config file must have a value.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            result = config_provider.get_releases_destination_with_mask_replaced(release_model, 'mp3')

    @mock.patch('subprocess.call')
    def test__get_flac_path__flac_is_on_path__flac_returned(self, subprocess_mock):
        subprocess_mock.return_value = 0
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_flac_path()
        self.assertEqual('flac', result)
        subprocess_mock.assert_called_with(['which', 'flac'])

    @mock.patch('os.path.exists')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__flac_path_is_set_on_environment_variable__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = '/some/path/to/flac'
        path_exists_mock.return_value = True
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_flac_path()
        self.assertEqual('/some/path/to/flac', result)
        environ_mock.get.assert_called_with('FLAC_PATH')

    @mock.patch('os.path.exists')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__environment_variable_has_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = '/some/incorrect/path/to/flac'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        with self.assertRaisesRegexp(ConfigurationError, 'The path specified by FLAC_PATH is incorrect. Please provide a valid path for flac.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_path()

    @mock.patch('ConfigParser.ConfigParser.get')
    @mock.patch('os.path.exists')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__flac_is_in_config_file__returns_correct_path(self, subprocess_mock, environ_mock, path_exists_mock, config_get_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/some/path/to/flac'
        directory_selector_mock = Mock()
        directory_selector_mock.select_directory.return_value = 0
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_flac_path()
        self.assertEqual('/some/path/to/flac', result)
        config_get_mock.assert_called_with('encoding', 'flac_path')

    @mock.patch('ConfigParser.ConfigParser.read')
    @mock.patch('ConfigParser.ConfigParser.get')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__flac_is_in_config_file__correct_config_file_is_used(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/some/path/to/flac'
        config_provider.get_flac_path()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__config_file_does_not_exist__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_path()

    @mock.patch('ConfigParser.ConfigParser.read')
    @mock.patch('ConfigParser.ConfigParser.get')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('os.environ')
    @mock.patch('subprocess.call')
    def test__get_flac_path__config_file_specifies_incorrect_path__raises_configuration_error(self, subprocess_mock, environ_mock, expanduser_mock, path_exists_mock, config_get_mock, config_read_mock):
        subprocess_mock.return_value = 1
        environ_mock.get.return_value = None
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.side_effect = [True, False]
        config_get_mock.return_value = '/some/path/to/flac'
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The path specified for flac in the .amu_config file is incorrect. Please provide a valid path for flac.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_path()

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.get')
    def test__get_flac_encoding_setting__encoding_setting_is_in_config_file__returns_correct_value(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = '-5'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_flac_encoding_setting()
        self.assertEqual('-5', result)
        config_get_mock.assert_called_with('encoding', 'flac_encoding_setting')

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.get')
    def test__get_flac_encoding_setting__encoding_setting_is_empty__raises_configuration_error(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = ''
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'A value must be provided for the flac encoding setting.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_encoding_setting()

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.read')
    @mock.patch('ConfigParser.ConfigParser.get')
    @mock.patch('os.path.expanduser')
    def test__get_flac_encoding_setting__encoding_setting_is_in_config_file__correct_config_file_is_used(self, expanduser_mock, config_get_mock, config_read_mock, path_exists_mock):
        path_exists_mock.return_value = True
        expanduser_mock.return_value = '/home/user/'
        config_get_mock.return_value = '-5'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_flac_encoding_setting()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    def test__get_flac_encoding_setting__config_file_does_not_exist__raises_configuration_error(self, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_encoding_setting()

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.get')
    def test__get_flac_decode_setting__decode_setting_is_in_config_file__returns_correct_value(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = '-5'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        result = config_provider.get_flac_decode_setting()
        self.assertEqual('-5', result)
        config_get_mock.assert_called_with('encoding', 'flac_decode_setting')

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.get')
    def test__get_flac_decode_setting__decode_setting_is_empty__raises_configuration_error(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = ''
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'A value must be provided for the flac decode setting.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_decode_setting()

    @mock.patch('os.path.exists')
    @mock.patch('ConfigParser.ConfigParser.read')
    @mock.patch('ConfigParser.ConfigParser.get')
    @mock.patch('os.path.expanduser')
    def test__get_flac_decode_setting__encoding_setting_is_in_config_file__correct_config_file_is_used(self, expanduser_mock, config_get_mock, config_read_mock, path_exists_mock):
        path_exists_mock.return_value = True
        expanduser_mock.return_value = '/home/user/'
        config_get_mock.return_value = '-5'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_flac_decode_setting()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    def test__get_flac_decode_setting__config_file_does_not_exist__raises_configuration_error(self, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_flac_decode_setting()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_mixes_destination__config_file_has_mixes_directory__the_correct_config_value_is_read(self, config_get_mock, path_exists_mock):
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/path/to/mixes'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_mixes_destination()
        mask_call = config_get_mock.mock_calls[0]
        self.assertEqual('directories', mask_call[1][0])
        self.assertEqual('mixes_directory', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_mixes_destination__config_file_has_mixes_directory__the_correct_config_file_should_be_read(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '/path/to/mixes'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_mixes_destination()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_mixes_destination__mixes_directory_has_user_home_reference__the_mixes_directory_should_be_expanded(self, config_get_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user'
        path_exists_mock.return_value = True
        config_get_mock.return_value = '~/Music'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.get_mixes_destination()
        expanduser_call = expanduser_mock.mock_calls[1]
        self.assertEqual('~/Music', expanduser_call[1][0])

    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    def test__get_mixes_destination__config_file_does_not_exist__raises_configuration_error(self, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = False
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The .amu_config file does not exist in your home directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_mixes_destination()

    @mock.patch('os.path.exists')
    @mock.patch('os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__get_mixes_destination__mixes_directory_does_not_exist__raises_configuration_error(self, config_get_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user'
        path_exists_mock.side_effect = [True, False]
        config_get_mock.return_value = '~/Music'
        directory_selector_mock = Mock()
        with self.assertRaisesRegexp(ConfigurationError, 'The path specified for mixes_directory in the .amu_config file is incorrect. Please provide a valid path for mixes_directory.'):
            config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            config_provider.get_mixes_destination()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_use_genre_setting__the_correct_config_value_is_read(self, config_get_mock, expanduser_mock, path_exists_mock):
        config_get_mock.return_value = 'True'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.use_genre()
        mask_call = config_get_mock.mock_calls[0]
        self.assertEqual('tagging', mask_call[1][0])
        self.assertEqual('use_genre', mask_call[1][1])

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_use_genre_setting__the_correct_config_file_should_be_read(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = 'True'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        config_provider.use_genre()
        config_read_mock.assert_called_with('/home/user/.amu_config')

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_true_genre_setting__true_should_be_returned(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = 'true'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        self.assertTrue(config_provider.use_genre())

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_false_genre_setting__false_should_be_returned(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = 'false'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        self.assertFalse(config_provider.use_genre())

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_mixed_case_genre_setting__true_should_be_returned(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = 'True'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        self.assertTrue(config_provider.use_genre())

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.os.path.expanduser')
    @mock.patch('amu.config.ConfigParser.ConfigParser.read')
    @mock.patch('amu.config.ConfigParser.ConfigParser.get')
    def test__use_genre__config_file_has_yes_genre_setting__true_should_be_returned(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        expanduser_mock.return_value = '/home/user/'
        path_exists_mock.return_value = True
        config_get_mock.return_value = 'yes'
        directory_selector_mock = Mock()
        config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
        self.assertTrue(config_provider.use_genre())

    #@mock.patch('amu.config.os.path.exists')
    #@mock.patch('amu.config.os.path.expanduser')
    #@mock.patch('amu.config.ConfigParser.ConfigParser.read')
    #@mock.patch('amu.config.ConfigParser.ConfigParser.get')
    #def test__use_genre__config_file_has_non_boolean_use_genre_setting__it_should_raise_a_configuration_error(self, config_get_mock, config_read_mock, expanduser_mock, path_exists_mock):
        #with self.assertRaisesRegexp(ConfigurationError, 'A true or false value must be used for the use_genre setting.'):
            #expanduser_mock.return_value = '/home/user/'
            #path_exists_mock.return_value = True
            #config_get_mock.return_value = 'blah'
            #directory_selector_mock = Mock()
            #config_provider = ConfigurationProvider(MaskReplacer(), directory_selector_mock)
            #config_provider.use_genre()
