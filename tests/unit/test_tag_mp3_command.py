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
        with self.assertRaisesRegexp(CommandValidationError, 'The source must be an mp3, not a directory.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__source_does_not_exist__throws_command_validation_exception(self, config_mock, path_exists_mock):
        path_exists_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/non_existent.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The specified mp3 source does not exist.'):
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
        with self.assertRaisesRegexp(CommandValidationError, 'An artist must be supplied for the tag.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__album_is_not_supplied__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        with self.assertRaisesRegexp(CommandValidationError, 'An album must be supplied for the tag.'):
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
        command.album = 'Druqks'
        command.title = ''
        with self.assertRaisesRegexp(CommandValidationError, 'A title must be supplied for the tag.'):
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
        command.album = 'Druqks'
        command.track_number = 0
        with self.assertRaisesRegexp(CommandValidationError, 'The track number must be at least 1.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__validate__track_no_is_greater_than_total__throws_command_validation_exception(self, config_mock, isdir_mock, path_exists_mock):
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = TagMp3Command(config_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = 'Flap Head'
        command.album = 'Druqks'
        command.track_number = 3
        command.track_total = 2
        with self.assertRaisesRegexp(CommandValidationError, 'The track number cannot be greater than the track total.'):
            command.validate()
