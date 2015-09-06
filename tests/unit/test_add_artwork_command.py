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
            command.source = '/path/to/audio.mp3'
            command.validate()

    @mock.patch('os.path.exists')
    def test__validate__destination_does_not_exist__raises_command_validation_error(self, exists_mock):
        exists_mock.return_value = True
        with self.assertRaisesRegexp(CommandValidationError, 'A destination must be supplied for the add artwork command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = AddArtworkCommand(config_mock, tagger_mock)
            command.source = '/path/to/audio.mp3'
            command.destination = ''
            command.validate()
