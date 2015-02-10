import mock
import unittest
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command
from amu.commands.ripcdcommand import RipCdCommand
from amu.parsing import CommandParsingError
from amu.parsing import EncodeCommandParser

class EncodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_and_destination_are_files__returns_single_encode_wav_to_mp3_command(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = True
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/song.wav', '/some/path/to/song.mp3')
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], EncodeWavToMp3Command)
        self.assertEqual('/some/path/to/song.wav', commands[0].source)
        self.assertEqual('/some/path/to/song.mp3', commands[0].destination)

    @mock.patch('os.path.exists')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_does_not_exist__throws_command_parsing_exception(self, config_mock, cd_ripper_mock, encoder_mock, exists_mock):
        exists_mock.return_value = False
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory or wav file must exist'):
            parser.parse_wav_to_mp3('/some/path/to/song.wav', '/some/path/to/song.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_is_directory_with_4_wav_files__returns_4_correctly_specified_encode_wav_to_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_is_multi_cd_release__returns_8_correctly_specified_encode_wav_to_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', ('cd1', 'cd2'), ()),
            ('/some/path/to/wavs/cd1', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav')),
            ('/some/path/to/wavs/cd2', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(8, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/cd1/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/cd1/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/cd1/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/cd1/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.mp3')
        self.assertEqual(commands[4].source, '/some/path/to/wavs/cd2/01 - Track 1.wav')
        self.assertEqual(commands[4].destination, '/some/destination/cd2/01 - Track 1.mp3')
        self.assertEqual(commands[5].source, '/some/path/to/wavs/cd2/02 - Track 2.wav')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/02 - Track 2.mp3')
        self.assertEqual(commands[6].source, '/some/path/to/wavs/cd2/03 - Track 3.wav')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/03 - Track 3.mp3')
        self.assertEqual(commands[7].source, '/some/path/to/wavs/cd2/04 - Track 4.wav')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/04 - Track 4.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_contains_files_that_are_not_wavs__commands_should_not_be_generated_for_non_wav_files(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', 'rip.log', 'description.txt'))
        ]
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav_to_mp3('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))

    @mock.patch('os.path.exists')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__destination_is_empty__throws_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, exists_mock):
        exists_mock.return_value = True
        with self.assertRaisesRegexp(CommandParsingError, 'The destination cannot be empty'):
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_wav_to_mp3('/some/path/to/song.wav', '')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_wav_to_mp3__source_is_file_but_destination_is_directory__throws_command_parsing_error(self, config_mock, cd_ripper_mock, encoder_mock, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = True
        with self.assertRaisesRegexp(CommandParsingError, 'If the source is a file, the destination must also be a file.'):
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_wav_to_mp3('/some/path/to/song.wav', '/some/destination/')

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_cd_to_mp3__cd_has_5_tracks__it_should_generate_a_correctly_specified_rip_cd_command_and_5_correctly_specified_encode_wav_to_mp3_commands(self, config_mock, cd_ripper_mock, encoder_mock):
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_cd_rip('/tmp/rip/destination', '/some/destination', 5)
        self.assertEqual(6, len(commands))
        self.assertIsInstance(commands[0], RipCdCommand)
        self.assertEqual(commands[0].destination, '/tmp/rip/destination')
        self.assertIsInstance(commands[1], EncodeWavToMp3Command)
        self.assertEqual(commands[1].source, '/tmp/rip/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].destination, '/some/destination/01 - Track 1.mp3')
        self.assertIsInstance(commands[2], EncodeWavToMp3Command)
        self.assertEqual(commands[2].source, '/tmp/rip/destination/02 - Track 2.wav')
        self.assertEqual(commands[2].destination, '/some/destination/02 - Track 2.mp3')
        self.assertIsInstance(commands[3], EncodeWavToMp3Command)
        self.assertEqual(commands[3].source, '/tmp/rip/destination/03 - Track 3.wav')
        self.assertEqual(commands[3].destination, '/some/destination/03 - Track 3.mp3')
        self.assertIsInstance(commands[4], EncodeWavToMp3Command)
        self.assertEqual(commands[4].source, '/tmp/rip/destination/04 - Track 4.wav')
        self.assertEqual(commands[4].destination, '/some/destination/04 - Track 4.mp3')
        self.assertIsInstance(commands[5], EncodeWavToMp3Command)
        self.assertEqual(commands[5].source, '/tmp/rip/destination/05 - Track 5.wav')
        self.assertEqual(commands[5].destination, '/some/destination/05 - Track 5.mp3')

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_cd_to_mp3__cd_has_12_tracks__the_track_numbers_should_be_padded_correctly(self, config_mock, cd_ripper_mock, encoder_mock):
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_cd_rip('/tmp/rip/destination', '/some/destination', 12)
        self.assertEqual(13, len(commands))
        self.assertEqual(commands[1].source, '/tmp/rip/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[10].source, '/tmp/rip/destination/10 - Track 10.wav')
        self.assertEqual(commands[10].destination, '/some/destination/10 - Track 10.mp3')

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_cd_to_mp3__rip_destination_is_empty__throws_command_parsing_exception(self, config_mock, cd_ripper_mock, encoder_mock):
        with self.assertRaisesRegexp(CommandParsingError, 'The rip destination cannot be empty'):
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_cd_rip('', '/some/destination', 5)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    @mock.patch('amu.rip.RubyRipperCdRipper')
    def test__parse_cd_to_mp3__destination_is_empty__throws_command_parsing_exception(self, config_mock, cd_ripper_mock, encoder_mock):
        with self.assertRaisesRegexp(CommandParsingError, 'The destination cannot be empty'):
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_cd_rip('/tmp/rip/destination', '', 5)
