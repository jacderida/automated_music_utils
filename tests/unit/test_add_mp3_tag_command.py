""" Test suite for the tag mp3 command. """
import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import AddMp3TagCommand
from mock import Mock


class AddMp3TagCommandTest(unittest.TestCase):
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    def test__validate__source_is_directory__throws_command_validation_exception(self, isdir_mock, path_exists_mock):
        config_mock = Mock()
        path_exists_mock.return_value = True
        isdir_mock.return_value = True
        command = AddMp3TagCommand(config_mock)
        command.source = '/Music/album'
        with self.assertRaisesRegexp(CommandValidationError, 'The source must be an mp3, not a directory.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    def test__validate__source_does_not_exist__throws_command_validation_exception(self, path_exists_mock):
        config_mock = Mock()
        path_exists_mock.return_value = False
        command = AddMp3TagCommand(config_mock)
        command.source = '/Music/album/non_existent.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The specified mp3 source does not exist.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    def test__validate__track_no_is_less_than_1__throws_command_validation_exception(self, isdir_mock, path_exists_mock):
        config_mock = Mock()
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = AddMp3TagCommand(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = 'Flap Head'
        command.album = 'Druqks'
        command.track_number = 0
        with self.assertRaisesRegexp(CommandValidationError, 'The track number must be at least 1.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    def test__validate__track_no_is_greater_than_total__throws_command_validation_exception(self, isdir_mock, path_exists_mock):
        config_mock = Mock()
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = AddMp3TagCommand(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = 'Flap Head'
        command.album = 'Druqks'
        command.track_number = 3
        command.track_total = 2
        with self.assertRaisesRegexp(CommandValidationError, 'The track number cannot be greater than the track total.'):
            command.validate()
