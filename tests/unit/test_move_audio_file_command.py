import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import MoveAudioFileCommand


class MoveAudioFileCommandTest(unittest.TestCase):
    @mock.patch('os.rename')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__valid_source_and_destination__file_is_moved(self, config_mock, rename_mock):
        command = MoveAudioFileCommand(config_mock)
        command.source = '/some/mp3/source/01 - Track 1.mp3'
        command.destination = '/some/other/mp3/destination/01 - Track 1.mp3'
        command.execute()
        rename_mock.assert_called_once_with('/some/mp3/source/01 - Track 1.mp3', '/some/other/mp3/destination/01 - Track 1.mp3')
