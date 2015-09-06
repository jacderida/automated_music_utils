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
