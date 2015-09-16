import mock
import unittest
from mock import Mock
from amu.commands import AddArtworkCommand
from amu.commands import CommandValidationError


class AddArtworkCommandTest(unittest.TestCase):
    def test__validate__source_is_empty__raises_command_validation_error(self):
        with self.assertRaisesRegexp(CommandValidationError, 'A source must be supplied for the add artwork command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = AddArtworkCommand(config_mock, tagger_mock)
            command.source = ''
            command.validate()

    @mock.patch('os.path.exists')
    def test__validate__source_does_not_exist__raises_command_validation_error(self, exists_mock):
        exists_mock.return_value = False
        with self.assertRaisesRegexp(CommandValidationError, 'A valid source must be supplied for the add artwork command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = AddArtworkCommand(config_mock, tagger_mock)
            command.source = '/path/to/cover.jpg'
            command.validate()

    @mock.patch('os.path.exists')
    def test__validate__destination_is_empty__raises_command_validation_error(self, exists_mock):
        exists_mock.return_value = True
        with self.assertRaisesRegexp(CommandValidationError, 'A destination must be supplied for the add artwork command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = AddArtworkCommand(config_mock, tagger_mock)
            command.source = '/path/to/cover.jpg'
            command.destination = ''
            command.validate()

    @mock.patch('os.path.exists')
    def test__validate__destination_does_not_exist__raises_command_validation_error(self, exists_mock):
        exists_mock.side_effect = [True, False]
        with self.assertRaisesRegexp(CommandValidationError, 'A valid destination must be supplied for the add artwork command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = AddArtworkCommand(config_mock, tagger_mock)
            command.source = '/path/to/cover.jpg'
            command.destination = '/path/to/audio.mp3'
            command.validate()

    def test__execute__valid_source_and_destination__calls_tagger_to_apply_artwork(self):
        config_mock, tagger_mock = (Mock(),)*2
        command = AddArtworkCommand(config_mock, tagger_mock)
        command.source = '/path/to/cover.jpg'
        command.destination = '/path/to/audio.mp3'
        command.execute()
        tagger_mock.apply_artwork.assert_called_once_with('/path/to/cover.jpg', '/path/to/audio.mp3')
