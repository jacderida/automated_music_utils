import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import MoveAudioFileCommand


class MoveAudioFileCommandTest(unittest.TestCase):
    @mock.patch('os.rename')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__valid_source_and_destination__file_is_moved(self, config_mock, rename_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        command.execute()
        rename_mock.assert_called_once_with('/some/mp3/source/01 - Track 1.mp3', '/some/other/mp3/destination/01 - Track 1.mp3')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_is_empty__raises_command_validation_error(self, config_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = ''
        with self.assertRaisesRegexp(CommandValidationError, 'A source must be supplied for the move audio file command.'):
            command.validate()

    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__destination_is_empty__raises_command_validation_error(self, config_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = ''
        with self.assertRaisesRegexp(CommandValidationError, 'A destination must be supplied for the move audio file command.'):
            command.validate()
