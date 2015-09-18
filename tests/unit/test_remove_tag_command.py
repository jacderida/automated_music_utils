import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import RemoveTagCommand
from mock import Mock


class RemoveTagCommandTest(unittest.TestCase):
    def test__validate__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be specified for the remove tag command.'):
            config_mock, tagger_mock = (Mock(),)*2
            command = RemoveTagCommand(config_mock, tagger_mock)
            command.validate()

    @mock.patch('os.path.exists')
    def test__validate__source_is_does_not_exist__raises_command_validation_error(self, path_exists_mock):
        with self.assertRaisesRegexp(CommandValidationError, 'The specified source does not exist.'):
            path_exists_mock.return_value = False
            config_mock, tagger_mock = (Mock(),)*2
            command = RemoveTagCommand(config_mock, tagger_mock)
            command.source = '/some/path/to/source.mp3'
            command.validate()

    def test__execute__valid_source__tagger_is_called_to_remove_tag(self):
        config_mock, tagger_mock = (Mock(),)*2
        command = RemoveTagCommand(config_mock, tagger_mock)
        command.source = '/some/path/to/source.mp3'
        command.execute()
        tagger_mock.remove_tags.assert_called_once_with('/some/path/to/source.mp3')
