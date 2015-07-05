""" Test suite for the tag mp3 command. """
import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import TagMp3Command


class TagMp3CommandTest(unittest.TestCase):
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_is_directory__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = True
        command = TagMp3Command(config_mock)
        command.source = '/Music/album'
        with self.assertRaises(CommandValidationError):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_does_not_exist__throws_command_validation_exception(self, config_mock, path_exists_mock):
        path_exists_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/non_existent.mp3'
        with self.assertRaises(CommandValidationError):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__artist_is_not_supplied__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = ''
        with self.assertRaises(CommandValidationError):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__title_is_not_supplied__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = ''
        with self.assertRaises(CommandValidationError):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__track_no_is_less_than_1__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = 'Flap Head'
        command.track_number = 0
        with self.assertRaises(CommandValidationError):
            command.validate()
