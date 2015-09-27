import mock
import unittest
from amu.commands import CommandValidationError
from amu.commands import DecodeAudioCommand
from mock import Mock


class DecodeAudioCommandTest(unittest.TestCase):
    def test__validate__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be specified for decoding an audio file'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.destination = '/some/destination'
            command.validate()

    def test__validate__destination_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A destination must be specified for decoding an audio file'):
            config_mock, encoder_mock = (Mock(),)*2
            command = DecodeAudioCommand(config_mock, encoder_mock)
            command.source = '/some/source'
            command.validate()
