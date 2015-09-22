""" Test suite for the tag mp3 command. """
import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import AddTagCommand
from mock import Mock


class AddTagCommandTest(unittest.TestCase):
    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    def test__validate__source_is_directory__throws_command_validation_exception(self, isdir_mock, path_exists_mock):
        config_mock, tagger_mock = (Mock(),)*2
        path_exists_mock.return_value = True
        isdir_mock.return_value = True
        command = AddTagCommand(config_mock, tagger_mock)
        command.source = '/Music/album'
        with self.assertRaisesRegexp(CommandValidationError, 'The source must be an mp3, not a directory.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    def test__validate__source_does_not_exist__throws_command_validation_exception(self, path_exists_mock):
        config_mock, tagger_mock = (Mock(),)*2
        path_exists_mock.return_value = False
        command = AddTagCommand(config_mock, tagger_mock)
        command.source = '/Music/album/non_existent.mp3'
        with self.assertRaisesRegexp(CommandValidationError, 'The specified mp3 source does not exist.'):
            command.validate()

    @mock.patch('amu.config.os.path.exists')
    @mock.patch('os.path.isdir')
    def test__validate__track_no_is_less_than_1__throws_command_validation_exception(self, isdir_mock, path_exists_mock):
        config_mock, tagger_mock = (Mock(),)*2
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = AddTagCommand(config_mock, tagger_mock)
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
        config_mock, tagger_mock = (Mock(),)*2
        path_exists_mock.return_value = True
        isdir_mock.return_value = False
        command = AddTagCommand(config_mock, tagger_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.title = 'Flap Head'
        command.album = 'Druqks'
        command.track_number = 3
        command.track_total = 2
        with self.assertRaisesRegexp(CommandValidationError, 'The track number cannot be greater than the track total.'):
            command.validate()

    def test__execute__valid_command_specified__tagger_is_called(self):
        config_mock, tagger_mock = (Mock(),)*2
        command = AddTagCommand(config_mock, tagger_mock)
        command.source = '/Music/album/song.mp3'
        command.artist = 'Aphex Twin'
        command.album_artist = 'Various'
        command.title = 'Flap Head'
        command.album = 'Druqks'
        command.genre = 'Electronic'
        command.year = '2015'
        command.comment = 'WarpCD92'
        command.track_number = 3
        command.track_total = 4
        command.disc_number = 2
        command.disc_total = 3
        command.execute()
        tagger_mock.add_tags.assert_called_once_with(
            '/Music/album/song.mp3', 'Aphex Twin', 'Various', 'Druqks', 'Flap Head', '2015', 'Electronic', 'WarpCD92', 3, 4, 2, 3)
