import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import RemoveTagCommand
from mock import Mock


class RemoveTagCommandTest(unittest.TestCase):
    def test__validate__source_is_empty__raises_command_validation_error(self):
        with self.assertRaisesRegexp(CommandValidationError, 'A source must be specified for the remove tag command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = RemoveTagCommand(config_mock, tagger_mock)
            command.validate()
