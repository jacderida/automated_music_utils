import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import DecodeAudioCommand
from mock import Mock


class DecodeAudioCommandTest(unittest.TestCase):
    def test__validate__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be specified for decoding an audio file'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.destination = '/some/destination'
            command.validate()

    def test__validate__destination_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A destination must be specified for decoding an audio file'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.source = '/some/source'
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    def test__validate__source_is_non_existent__raises_command_validation_error(self, path_exists_mock):
        path_exists_mock.return_value = False
        with self.assertRaisesRegexp(CommandValidationError, 'The specified source does not exist.'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.source = '/some/source'
            command.destination = '/some/destination'
            command.validate()

    @mock.patch('amu.config.os.path.isdir')
    @mock.patch('amu.config.os.path.exists')
    def test__validate__source_is_directory__raises_command_validation_error(self, path_exists_mock, isdir_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = True
        with self.assertRaisesRegexp(CommandValidationError, 'The source cannot be a directory.'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.source = '/some/source/'
            command.destination = '/some/destination/'
            command.validate()

    @mock.patch('os.remove')
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    def test__execute__encoder_called_correctly__is_called_with_correct_arguments(self, makedirs_mock, path_exists_mock, remove_mock):
        path_exists_mock.return_value = True
        config_mock, encoder_mock = (Mock(),)*2
        command = DecodeAudioCommand(config_mock, encoder_mock)
        command.source = '/some/source'
        command.destination = '/some/destination'
        command.execute()
        encoder_mock.decode.assert_called_once_with('/some/source', '/some/destination')
