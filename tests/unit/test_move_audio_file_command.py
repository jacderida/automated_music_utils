import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import MoveAudioFileCommand


class MoveAudioFileCommandTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.rename')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__valid_source_and_destination__file_is_moved(self, config_mock, rename_mock, exists_mock):
        exists_mock.return_value = True
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        command.execute()
        rename_mock.assert_called_once_with('/some/mp3/source/01 - Track 1.mp3', '/some/other/mp3/destination/01 - Track 1.mp3')

    @mock.patch('os.makedirs')
    @mock.patch('os.rename')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__destination_directory_does_not_exist__destination_directories_are_created(self, config_mock, rename_mock, makedirs_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        command.execute()
        makedirs_mock.assert_called_once_with('/some/other/mp3/destination')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_is_empty__raises_command_validation_error(self, config_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = ''
        with self.assertRaisesRegexp(CommandValidationError, 'A source must be supplied for the move audio file command.'):
            command.validate()

    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__destination_is_empty__raises_command_validation_error(self, config_mock, exists_mock, isdir_mock):
        isdir_mock.return_value = False
        exists_mock.return_value = True
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = ''
        with self.assertRaisesRegexp(CommandValidationError, 'A destination must be supplied for the move audio file command.'):
            command.validate()

    @mock.patch('os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_does_not_exist__raises_command_validation_error(self, config_mock, exists_mock):
        exists_mock.return_value = False
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The source for the move audio file command must exist.'):
            command.validate()

    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_and_destination_have_different_extensions__raises_command_validation_error(self, config_mock, exists_mock, isdir_mock):
        isdir_mock.return_value = False
        exists_mock.return_value = True
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.wav'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The move audio file command must operate on files of the same type.'):
            command.validate()

    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_is_directory__raises_command_validation_error(self, config_mock, exists_mock, isdir_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = True
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The source for the move audio file command cannot be a directory.'):
            command.validate()
