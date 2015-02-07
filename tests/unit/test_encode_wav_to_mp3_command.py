import mock
import unittest
from amu.commands.command import CommandValidationError
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command

class EncodeWavToMp3CommandTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__execute__encoder_called_correctly__is_called_with_correct_arguments(self, config_mock, encoder_mock, makedirs_mock, path_exists_mock):
        path_exists_mock.return_value = True
        command = EncodeWavToMp3Command(config_mock, encoder_mock)
        command.source = '/some/source'
        command.destination = '/some/destination'
        command.execute()
        encoder_mock.encode_wav_to_mp3.assert_called_once_with('/some/source', '/some/destination')

    @mock.patch('os.path.exists')
    @mock.patch('os.makedirs')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__execute__destination_directory_does_not_exist__destination_directory_is_created(self, config_mock, encoder_mock, makedirs_mock, path_exists_mock):
        path_exists_mock.return_value = False
        command = EncodeWavToMp3Command(config_mock, encoder_mock)
        command.source = '/some/source'
        command.destination = '/some/destination/with/many/sub/directories/mp3'
        command.execute()
        makedirs_mock.assert_called_once_with('/some/destination/with/many/sub/directories')

    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__validate__source_is_empty__throws_command_validation_exception(self, config_mock, encoder_mock):
        with self.assertRaisesRegexp(CommandValidationError, 'A source must be specified for encoding a wav to mp3'):
            command = EncodeWavToMp3Command(config_mock, encoder_mock)
            command.destination = '/some/destination'
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__validate__source_is_non_existent__throws_command_validation_exception(self, config_mock, encoder_mock, path_exists_mock):
        path_exists_mock.return_value = False
        with self.assertRaisesRegexp(CommandValidationError, 'The specified source does not exist.'):
            command = EncodeWavToMp3Command(config_mock, encoder_mock)
            command.source = '/some/source'
            command.destination = '/some/destination'
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__validate__destination_is_empty__throws_command_validation_exception(self, config_mock, encoder_mock, path_exists_mock):
        path_exists_mock.return_value = True
        with self.assertRaisesRegexp(CommandValidationError, 'A destination must be specified for encoding a wav to mp3'):
            command = EncodeWavToMp3Command(config_mock, encoder_mock)
            command.source = '/some/source'
            command.validate()

    @mock.patch('amu.config.os.path.isdir')
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.encode.LameEncoder')
    def test__validate__source_is_directory__throws_command_validation_exception(self, config_mock, encoder_mock, path_exists_mock, isdir_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = True
        with self.assertRaisesRegexp(CommandValidationError, 'The source cannot be a directory.'):
            command = EncodeWavToMp3Command(config_mock, encoder_mock)
            command.source = '/some/source/'
            command.validate()
