import unittest
from mock import Mock
from amu.commands import CommandValidationError
from amu.commands import FetchReleaseCommand


class FetchReleaseCommandTest(unittest.TestCase):
    def test__validate__a_non_integter_is_used_for_the_id__raises_command_validation_error(self):
        with self.assertRaisesRegexp(CommandValidationError, 'The fetch command must use a valid integer for the discogs ID.'):
            config_service_mock = Mock()
            metadata_service_mock = Mock()
            command = FetchReleaseCommand(config_service_mock, metadata_service_mock)
            command.discogs_id = 'invalid'
            command.validate()
