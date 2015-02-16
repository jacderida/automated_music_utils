""" Test suite for the command parser. """
import mock
import os
import unittest
import uuid
from amu import utils
from amu.clidriver import CliDriver
from amu.commands import RipCdCommand
from amu.commands import EncodeWavToMp3Command
from amu.parsing import CommandParser
from amu.parsing import CommandParsingError


class CommandParserTest(unittest.TestCase):
    """ Test suite for the command parser. """
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_rip_cd_is_specified__command_parser_returns_rip_cd_command(self, config_mock, cd_ripper_mock, encoder_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        command = parser.from_args(args)[0]
        self.assertIsInstance(command, RipCdCommand)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__rip_cd_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        command = parser.from_args(args)[0]
        self.assertEqual(os.getcwd(), command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__rip_cd_command_optional_destination__destination_should_be_optional_destination(self, config_mock, cd_ripper_mock, encoder_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip', '--destination=/some/path'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        command = parser.from_args(args)[0]
        self.assertEqual('/some/path', command.destination)

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_encode_from_wav_to_mp3_is_specified__it_should_use_the_encoder_command_parser(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'wav',
            'mp3',
            '--source=/some/song.wav',
            '--destination=some/song.mp3'
        ])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with('/some/song.wav', 'some/song.mp3')
        self.assertEqual(1, len(commands))

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_with_no_optional_source__source_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_with_optional_source__source_should_be_set_correctly(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--source=/some/source'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with('/some/source', os.getcwd())

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_with_optional_destination__destination_should_be_set_correctly(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--destination=/some/destination'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(os.getcwd(), '/some/destination')

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_with_keep_source_set__keep_source_should_be_true(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--keep-source'])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)
        self.assertTrue(commands[0].keep_source)
        self.assertTrue(commands[1].keep_source)

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_without_keep_source_specified__keep_source_should_be_false(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)
        self.assertFalse(commands[0].keep_source)
        self.assertFalse(commands[1].keep_source)

    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_wav_to_mp3_command_when_there_are_no_wavs_to_encode__throws_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = []
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory has no wavs to encode'):
            parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.from_args(args)

    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_encode_cd_to_mp3_command_is_specified__it_should_use_the_encoder_command_parser(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'cd',
            'mp3',
            '--destination=/some/destination'
        ])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 2
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(utils.AnyStringWith('/tmp'), '/some/destination', 2)
        self.assertEqual(3, len(commands))
        self.assertIsInstance(commands[0], RipCdCommand)
        self.assertIsInstance(commands[1], EncodeWavToMp3Command)
        self.assertIsInstance(commands[2], EncodeWavToMp3Command)

    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_encode_cd_to_mp3_command_is_specified__it_should_use_a_directory_with_a_guid_for_the_rip_destination(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'cd',
            'mp3',
            '--destination=/some/destination'
        ])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 2
        stored_args_mock = utils.get_mock_with_stored_call_args(encode_command_parser_mock)
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        temp_path = stored_args_mock.call_args[0][0]
        parsed_uuid = temp_path.split('/tmp/')[1]
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_cd_to_mp3_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'cd', 'mp3'])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 2
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(utils.AnyStringWith('/tmp'), os.getcwd(), 2)

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_cd_to_mp3_command_with_keep_source_set__keep_source_should_be_true(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'cd',
            'mp3',
            '--keep-source'
        ])
        number_of_tracks_mock.return_value = 2
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        self.assertTrue(commands[1].keep_source)
        self.assertTrue(commands[2].keep_source)

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__encode_rip_to_mp3_command_without_keep_source_specified__keep_source_should_be_false(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'cd', 'mp3'])
        number_of_tracks_mock.return_value = 2
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.from_args(args)
        self.assertFalse(commands[1].keep_source)
        self.assertFalse(commands[2].keep_source)
