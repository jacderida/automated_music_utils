""" Test suite for the command parser. """
import mock
import os
import unittest
from amu.clidriver import CliDriver
from amu.parsing import CommandParser
from amu.parsing import CommandParsingError
from amu.commands.ripcdcommand import RipCdCommand
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command


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
