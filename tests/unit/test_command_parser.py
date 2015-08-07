""" Test suite for the command parser. """
import mock
import os
import unittest
import uuid
from amu import utils
from amu.clidriver import CliDriver
from amu.commands import RipCdCommand
from amu.commands import EncodeWavToMp3Command
from amu.commands import AddMp3TagCommand
from amu.models import ReleaseModel
from amu.parsing import CommandParser
from amu.parsing import CommandParsingError


class CommandParserTest(unittest.TestCase):
    """ Test suite for the command parser. """
    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__when_rip_cd_is_specified__command_parser_returns_rip_cd_command(self, config_mock, cd_ripper_mock, encoder_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        command = parser.from_args(args)[0]
        self.assertIsInstance(command, RipCdCommand)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__rip_cd_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        command = parser.from_args(args)[0]
        self.assertEqual(os.getcwd(), command.destination)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__rip_cd_command_optional_destination__destination_should_be_optional_destination(self, config_mock, cd_ripper_mock, encoder_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['rip', '--destination=/some/path'])
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        command = parser.from_args(args)[0]
        self.assertEqual('/some/path', command.destination)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__when_encode_from_wav_to_mp3_is_specified__it_should_use_the_encoder_command_parser(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
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
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with('/some/song.wav', 'some/song.mp3')
        self.assertEqual(1, len(commands))

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_no_optional_source__source_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_optional_source__source_should_be_set_correctly(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--source=/some/source'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with('/some/source', os.getcwd())

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_optional_destination__destination_should_be_set_correctly(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--destination=/some/destination'])
        encode_command_parser_mock.return_value = [EncodeWavToMp3Command(config_mock, encoder_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(os.getcwd(), '/some/destination')

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_keep_source_set__keep_source_should_be_true(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3', '--keep-source'])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)
        self.assertTrue(commands[0].keep_source)
        self.assertTrue(commands[1].keep_source)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_without_keep_source_specified__keep_source_should_be_false(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        current_working_directory = os.getcwd()
        encode_command_parser_mock.assert_called_once_with(current_working_directory, current_working_directory)
        self.assertFalse(commands[0].keep_source)
        self.assertFalse(commands[1].keep_source)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_when_there_are_no_wavs_to_encode__throws_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'wav', 'mp3'])
        encode_command_parser_mock.return_value = []
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory has no wavs to encode'):
            parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
            parser.from_args(args)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_discogs_id_specified__it_should_return_4_tag_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'wav',
            'mp3',
            '--source=/some/path/to/wavs',
            '--destination=/some/path/to/mp3s',
            '--discogs-id=451034'
        ])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]

        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = [x for x in parser.from_args(args) if type(x) == AddMp3TagCommand]
        self.assertEqual(4, len(commands))

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_with_discogs_id_specified__the_sources_from_the_encode_commands_should_be_used(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'wav',
            'mp3',
            '--source=/some/path/to/wavs',
            '--destination=/some/path/to/mp3s',
            '--discogs-id=451034'
        ])
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/some/path/to/wavs/01 - Track 01.wav'
        command1.destination = '/some/path/to/mp3s/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/some/path/to/wavs/02 - Track 02.wav'
        command2.destination = '/some/path/to/mp3s/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/some/path/to/wavs/03 - Track 03.wav'
        command3.destination = '/some/path/to/mp3s/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/some/path/to/wavs/04 - Track 04.wav'
        command4.destination = '/some/path/to/mp3s/04 - Track 04.mp3'
        commands.append(command4)
        encode_command_parser_mock.return_value = commands

        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = [x for x in parser.from_args(args) if type(x) == AddMp3TagCommand]
        self.assertEqual('/some/path/to/mp3s/01 - Track 01.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 02.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 03.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 04.mp3', commands[3].source)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_wav_to_mp3')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_wav_to_mp3_command_discogs_release_and_cd_have_different_lengths__it_should_raise_a_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'wav',
            'mp3',
            '--source=/some/path/to/wavs',
            '--destination=/some/path/to/mp3s',
            '--discogs-id=451034'
        ])
        encode_command_parser_mock.return_value = [
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]

        release_model = ReleaseModel()
        release_model.artist = 'AFX'
        release_model.title = 'Analord 08'
        release_model.label = 'Rephlex'
        release_model.catno = 'ANALORD 08'
        release_model.format = 'Vinyl'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Breakbeat, House, Acid, Electro'
        release_model.add_track_directly(None, 'PWSteal.Ldpinch.D', 1, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Berbew.Q', 2, 4, 1, 1)
        release_model.add_track_directly(None, 'W32.Deadcode.A', 3, 4, 1, 1)
        release_model.add_track_directly(None, 'Backdoor.Spyboter.A', 4, 4, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        with self.assertRaisesRegexp(CommandParsingError, 'The source has 5 tracks and the discogs release has 4. The number of tracks on both must be the same.'):
            parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
            parser.from_args(args)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__when_encode_cd_to_mp3_command_is_specified__it_should_use_the_encoder_command_parser(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock):
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
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(utils.AnyStringWith('/tmp'), '/some/destination', 2)
        self.assertEqual(3, len(commands))
        self.assertIsInstance(commands[0], RipCdCommand)
        self.assertIsInstance(commands[1], EncodeWavToMp3Command)
        self.assertIsInstance(commands[2], EncodeWavToMp3Command)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__when_encode_cd_to_mp3_command_is_specified__it_should_use_a_directory_with_a_guid_for_the_rip_destination(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock):
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
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        temp_path = stored_args_mock.call_args[0][0]
        parsed_uuid = temp_path.split('/tmp/')[1]
        self.assertEqual(4, uuid.UUID(parsed_uuid).get_version())

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_with_no_optional_destination__destination_should_be_current_working_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock):
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
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        encode_command_parser_mock.assert_called_once_with(utils.AnyStringWith('/tmp'), os.getcwd(), 2)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_with_keep_source_set__keep_source_should_be_true(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, metadata_mock):
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
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        self.assertTrue(commands[1].keep_source)
        self.assertTrue(commands[2].keep_source)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_rip_to_mp3_command_without_keep_source_specified__keep_source_should_be_false(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock,  metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'cd', 'mp3'])
        number_of_tracks_mock.return_value = 2
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        self.assertFalse(commands[1].keep_source)
        self.assertFalse(commands[2].keep_source)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_with_discogs_id_specified__it_should_return_12_tag_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'cd', 'mp3', '--discogs-id=3535'])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 12
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]

        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '...I Care Because You Do'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD30'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1995'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Techno, Ambient, Experimental, Acid'
        release_model.add_track_directly(None, 'Acrid Avid Jam Shred', 1, 12, 1, 1)
        release_model.add_track_directly(None, 'The Waxen Pith', 2, 12, 1, 1)
        release_model.add_track_directly(None, 'Wax The Nip', 3, 12, 1, 1)
        release_model.add_track_directly(None, 'Icct Hedral (Edit)', 4, 12, 1, 1)
        release_model.add_track_directly(None, 'Ventolin (Video Version)', 5, 12, 1, 1)
        release_model.add_track_directly(None, 'Come On You Slags!', 6, 12, 1, 1)
        release_model.add_track_directly(None, 'Start As You Mean To Go On', 7, 12, 1, 1)
        release_model.add_track_directly(None, 'Wet Tip Hen Ax', 8, 12, 1, 1)
        release_model.add_track_directly(None, 'Mookid', 9, 12, 1, 1)
        release_model.add_track_directly(None, 'Alberto Balsalm', 10, 12, 1, 1)
        release_model.add_track_directly(None, 'Cow Cud Is A Twin', 11, 12, 1, 1)
        release_model.add_track_directly(None, 'Next Heap With', 12, 12, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = [x for x in parser.from_args(args) if type(x) == AddMp3TagCommand]
        self.assertEqual(12, len(commands))

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_with_discogs_id_specified__add_tag_sources_should_be_specified_correctly(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'cd',
            'mp3',
            '--destination=/some/destination',
            '--discogs-id=3535'])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 12
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]

        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '...I Care Because You Do'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD30'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1995'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Techno, Ambient, Experimental, Acid'
        release_model.add_track_directly(None, 'Acrid Avid Jam Shred', 1, 12, 1, 1)
        release_model.add_track_directly(None, 'The Waxen Pith', 2, 12, 1, 1)
        release_model.add_track_directly(None, 'Wax The Nip', 3, 12, 1, 1)
        release_model.add_track_directly(None, 'Icct Hedral (Edit)', 4, 12, 1, 1)
        release_model.add_track_directly(None, 'Ventolin (Video Version)', 5, 12, 1, 1)
        release_model.add_track_directly(None, 'Come On You Slags!', 6, 12, 1, 1)
        release_model.add_track_directly(None, 'Start As You Mean To Go On', 7, 12, 1, 1)
        release_model.add_track_directly(None, 'Wet Tip Hen Ax', 8, 12, 1, 1)
        release_model.add_track_directly(None, 'Mookid', 9, 12, 1, 1)
        release_model.add_track_directly(None, 'Alberto Balsalm', 10, 12, 1, 1)
        release_model.add_track_directly(None, 'Cow Cud Is A Twin', 11, 12, 1, 1)
        release_model.add_track_directly(None, 'Next Heap With', 12, 12, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = [x for x in parser.from_args(args) if type(x) == AddMp3TagCommand]
        self.assertEqual('/some/destination/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/destination/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/destination/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/destination/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/destination/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/destination/06 - Track 6.mp3', commands[5].source)
        self.assertEqual('/some/destination/07 - Track 7.mp3', commands[6].source)
        self.assertEqual('/some/destination/08 - Track 8.mp3', commands[7].source)
        self.assertEqual('/some/destination/09 - Track 9.mp3', commands[8].source)
        self.assertEqual('/some/destination/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/destination/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/destination/12 - Track 12.mp3', commands[11].source)

    @mock.patch('amu.metadata.MaskReplacer.replace_directory_mask')
    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.rip.tempfile.gettempdir')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.parsing.EncodeCommandParser.parse_cd_rip')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_with_discogs_id_specified__the_mask_replacer_is_called_to_replace_the_directory(self, config_mock, cd_ripper_mock, encoder_mock, encode_command_parser_mock, number_of_tracks_mock, gettempdir_mock, metadata_mock, maskreplacer_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'encode',
            'cd',
            'mp3',
            '--destination=/some/destination',
            '--discogs-id=3535'])
        gettempdir_mock.return_value = '/tmp' # Mocking for platform agnosticism.
        number_of_tracks_mock.return_value = 12
        encode_command_parser_mock.return_value = [
            RipCdCommand(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock),
            EncodeWavToMp3Command(config_mock, encoder_mock)
        ]

        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '...I Care Because You Do'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD30'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1995'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Techno, Ambient, Experimental, Acid'
        release_model.add_track_directly(None, 'Acrid Avid Jam Shred', 1, 12, 1, 1)
        release_model.add_track_directly(None, 'The Waxen Pith', 2, 12, 1, 1)
        release_model.add_track_directly(None, 'Wax The Nip', 3, 12, 1, 1)
        release_model.add_track_directly(None, 'Icct Hedral (Edit)', 4, 12, 1, 1)
        release_model.add_track_directly(None, 'Ventolin (Video Version)', 5, 12, 1, 1)
        release_model.add_track_directly(None, 'Come On You Slags!', 6, 12, 1, 1)
        release_model.add_track_directly(None, 'Start As You Mean To Go On', 7, 12, 1, 1)
        release_model.add_track_directly(None, 'Wet Tip Hen Ax', 8, 12, 1, 1)
        release_model.add_track_directly(None, 'Mookid', 9, 12, 1, 1)
        release_model.add_track_directly(None, 'Alberto Balsalm', 10, 12, 1, 1)
        release_model.add_track_directly(None, 'Cow Cud Is A Twin', 11, 12, 1, 1)
        release_model.add_track_directly(None, 'Next Heap With', 12, 12, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        maskreplacer_mock.assert_called_once_with('/some/destination', release_model)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__from_args__encode_cd_to_mp3_command_discogs_release_and_cd_have_different_lengths__it_should_raise_a_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, number_of_tracks_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args(['encode', 'cd', 'mp3', '--discogs-id=3535'])
        number_of_tracks_mock.return_value = 11

        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '...I Care Because You Do'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD30'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1995'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Techno, Ambient, Experimental, Acid'
        release_model.add_track_directly(None, 'Acrid Avid Jam Shred', 1, 12, 1, 1)
        release_model.add_track_directly(None, 'The Waxen Pith', 2, 12, 1, 1)
        release_model.add_track_directly(None, 'Wax The Nip', 3, 12, 1, 1)
        release_model.add_track_directly(None, 'Icct Hedral (Edit)', 4, 12, 1, 1)
        release_model.add_track_directly(None, 'Ventolin (Video Version)', 5, 12, 1, 1)
        release_model.add_track_directly(None, 'Come On You Slags!', 6, 12, 1, 1)
        release_model.add_track_directly(None, 'Start As You Mean To Go On', 7, 12, 1, 1)
        release_model.add_track_directly(None, 'Wet Tip Hen Ax', 8, 12, 1, 1)
        release_model.add_track_directly(None, 'Mookid', 9, 12, 1, 1)
        release_model.add_track_directly(None, 'Alberto Balsalm', 10, 12, 1, 1)
        release_model.add_track_directly(None, 'Cow Cud Is A Twin', 11, 12, 1, 1)
        release_model.add_track_directly(None, 'Next Heap With', 12, 12, 1, 1)
        metadata_mock.get_release_by_id.return_value = release_model

        with self.assertRaisesRegexp(CommandParsingError, 'The source has 11 tracks and the discogs release has 12. The number of tracks on both must be the same.'):
            parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
            parser.from_args(args)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.TagCommandParser.parse_add_mp3_tag_command')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_add_mp3_tag_is_specified__the_tag_command_parser_should_be_used(self, cd_ripper_mock, config_mock, encoder_mock, tag_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist="Aphex Twin"',
            '--album="Druqks"',
            '--title="Vordhosbn"',
            '--year="2001"',
            '--genre="Electronic"',
            '--track-number=2',
            '--track-total=15'
        ])
        tag_command_parser_mock.return_value = [AddMp3TagCommand(config_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        commands = parser.from_args(args)
        tag_command_parser_mock.assert_called_once()
        self.assertEqual(1, len(commands))

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.TagCommandParser.parse_add_mp3_tag_command')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_add_mp3_tag_is_specified__the_tag_command_parser_should_be_called_with_the_correct_arguments(self, cd_ripper_mock, config_mock, encoder_mock, tag_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist="Aphex Twin"',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        tag_command_parser_mock.return_value = [AddMp3TagCommand(config_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        command_args = tag_command_parser_mock.call_args[0][0]
        self.assertEqual('Aphex Twin', command_args.artist)
        self.assertEqual('Druqks', command_args.album)
        self.assertEqual('Vordhosbn', command_args.title)
        self.assertEqual(2001, command_args.year)
        self.assertEqual('Electronic', command_args.genre)
        self.assertEqual(2, command_args.track_number)
        self.assertEqual(15, command_args.track_total)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('amu.parsing.TagCommandParser.parse_add_mp3_tag_command')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_add_mp3_tag_is_specified__the_tag_command_parser_should_be_called_with_the_correct_arguments(self, cd_ripper_mock, config_mock, encoder_mock, tag_command_parser_mock, metadata_mock):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist="Aphex Twin"',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        tag_command_parser_mock.return_value = [AddMp3TagCommand(config_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        command_args = tag_command_parser_mock.call_args[0][0]
        self.assertEqual('Aphex Twin', command_args.artist)
        self.assertEqual('Druqks', command_args.album)
        self.assertEqual('Vordhosbn', command_args.title)
        self.assertEqual(2001, command_args.year)
        self.assertEqual('Electronic', command_args.genre)
        self.assertEqual(2, command_args.track_number)
        self.assertEqual(15, command_args.track_total)

    @mock.patch('amu.metadata.DiscogsMetadataService')
    @mock.patch('os.getcwd')
    @mock.patch('amu.parsing.TagCommandParser.parse_add_mp3_tag_command')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__from_args__when_add_mp3_tag_is_specified_with_no_source__source_should_be_the_current_working_directory(self, cd_ripper_mock, config_mock, encoder_mock, tag_command_parser_mock, getcwd_mock, metadata_mock):
        getcwd_mock.return_value = '/some/current/working/directory'
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--artist="Aphex Twin"',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        tag_command_parser_mock.return_value = [AddMp3TagCommand(config_mock)]
        parser = CommandParser(config_mock, cd_ripper_mock, encoder_mock, metadata_mock)
        parser.from_args(args)
        command_args = tag_command_parser_mock.call_args[0][0]
        self.assertEqual('/some/current/working/directory', command_args.source)
