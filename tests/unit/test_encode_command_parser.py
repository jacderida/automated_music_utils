import mock
import unittest
from mock import Mock
from amu.commands import EncodeWavCommand, RipCdCommand
from amu.parsing import CommandParsingError, EncodeCommandParser

class EncodeCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_and_destination_are_files__returns_single_encode_wav_to_mp3_command(self, isfile_mock, exists_mock):
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        exists_mock.return_value = True
        isfile_mock.return_value = True
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/song.wav', '/some/path/to/song.mp3')
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], EncodeWavCommand)
        self.assertEqual('/some/path/to/song.wav', commands[0].source)
        self.assertEqual('/some/path/to/song.mp3', commands[0].destination)

    @mock.patch('os.path.exists')
    def test__parse_wav__source_does_not_exist__throws_command_parsing_exception(self, exists_mock):
        exists_mock.return_value = False
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'The source directory or wav file must exist'):
            parser.parse_wav('/some/path/to/song.wav', '/some/path/to/song.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_is_directory_with_4_wav_files__returns_4_correctly_specified_encode_wav_to_mp3_commands(self, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.mp3')

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_is_multi_cd_release__returns_9_correctly_specified_encode_wav_to_mp3_commands(self, isfile_mock, exists_mock, walk_mock, listdir_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', ('cd1', 'cd2'), ()),
            ('/some/path/to/wavs/cd1', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav')),
            ('/some/path/to/wavs/cd2', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav'],
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav']
        ]
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(9, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/cd1/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/cd1/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/cd1/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/cd1/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.mp3')
        self.assertEqual(commands[4].source, '/some/path/to/wavs/cd1/05 - Track 5.wav')
        self.assertEqual(commands[4].destination, '/some/destination/cd1/05 - Track 5.mp3')
        self.assertEqual(commands[5].source, '/some/path/to/wavs/cd2/01 - Track 1.wav')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/01 - Track 1.mp3')
        self.assertEqual(commands[6].source, '/some/path/to/wavs/cd2/02 - Track 2.wav')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/02 - Track 2.mp3')
        self.assertEqual(commands[7].source, '/some/path/to/wavs/cd2/03 - Track 3.wav')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/03 - Track 3.mp3')
        self.assertEqual(commands[8].source, '/some/path/to/wavs/cd2/04 - Track 4.wav')
        self.assertEqual(commands[8].destination, '/some/destination/cd2/04 - Track 4.mp3')

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_is_multi_cd_release_and_walk_returns_directories_and_files_in_arbitrary_order__returns_18_correctly_specified_encode_wav_to_mp3_commands(self, isfile_mock, exists_mock, walk_mock, listdir_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', ('cd4', 'cd1', 'cd3', 'cd2'), ()),
            ('/some/path/to/wavs/cd4', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav')),
            ('/some/path/to/wavs/cd1', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav')),
            ('/some/path/to/wavs/cd3', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav')),
            ('/some/path/to/wavs/cd2', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav'],
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav'],
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', '05 - Track 5.wav'],
            ['01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav']
        ]
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(18, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/cd1/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/cd1/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/cd1/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/cd1/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/cd1/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/cd1/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/cd1/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/cd1/04 - Track 4.mp3')
        self.assertEqual(commands[4].source, '/some/path/to/wavs/cd1/05 - Track 5.wav')
        self.assertEqual(commands[4].destination, '/some/destination/cd1/05 - Track 5.mp3')
        self.assertEqual(commands[5].source, '/some/path/to/wavs/cd2/01 - Track 1.wav')
        self.assertEqual(commands[5].destination, '/some/destination/cd2/01 - Track 1.mp3')
        self.assertEqual(commands[6].source, '/some/path/to/wavs/cd2/02 - Track 2.wav')
        self.assertEqual(commands[6].destination, '/some/destination/cd2/02 - Track 2.mp3')
        self.assertEqual(commands[7].source, '/some/path/to/wavs/cd2/03 - Track 3.wav')
        self.assertEqual(commands[7].destination, '/some/destination/cd2/03 - Track 3.mp3')
        self.assertEqual(commands[8].source, '/some/path/to/wavs/cd2/04 - Track 4.wav')
        self.assertEqual(commands[8].destination, '/some/destination/cd2/04 - Track 4.mp3')
        self.assertEqual(commands[9].source, '/some/path/to/wavs/cd3/01 - Track 1.wav')
        self.assertEqual(commands[9].destination, '/some/destination/cd3/01 - Track 1.mp3')
        self.assertEqual(commands[10].source, '/some/path/to/wavs/cd3/02 - Track 2.wav')
        self.assertEqual(commands[10].destination, '/some/destination/cd3/02 - Track 2.mp3')
        self.assertEqual(commands[11].source, '/some/path/to/wavs/cd3/03 - Track 3.wav')
        self.assertEqual(commands[11].destination, '/some/destination/cd3/03 - Track 3.mp3')
        self.assertEqual(commands[12].source, '/some/path/to/wavs/cd3/04 - Track 4.wav')
        self.assertEqual(commands[12].destination, '/some/destination/cd3/04 - Track 4.mp3')
        self.assertEqual(commands[13].source, '/some/path/to/wavs/cd3/05 - Track 5.wav')
        self.assertEqual(commands[13].destination, '/some/destination/cd3/05 - Track 5.mp3')
        self.assertEqual(commands[14].source, '/some/path/to/wavs/cd4/01 - Track 1.wav')
        self.assertEqual(commands[14].destination, '/some/destination/cd4/01 - Track 1.mp3')
        self.assertEqual(commands[15].source, '/some/path/to/wavs/cd4/02 - Track 2.wav')
        self.assertEqual(commands[15].destination, '/some/destination/cd4/02 - Track 2.mp3')
        self.assertEqual(commands[16].source, '/some/path/to/wavs/cd4/03 - Track 3.wav')
        self.assertEqual(commands[16].destination, '/some/destination/cd4/03 - Track 3.mp3')
        self.assertEqual(commands[17].source, '/some/path/to/wavs/cd4/04 - Track 4.wav')
        self.assertEqual(commands[17].destination, '/some/destination/cd4/04 - Track 4.mp3')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_contains_files_that_are_not_wavs__commands_should_not_be_generated_for_non_wav_files(self, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('01 - Track 1.wav', '02 - Track 2.wav', '03 - Track 3.wav', '04 - Track 4.wav', 'rip.log', 'description.txt'))
        ]
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))

    @mock.patch('os.path.exists')
    def test__parse_wav__destination_is_empty__throws_command_parsing_error(self, exists_mock):
        exists_mock.return_value = True
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        with self.assertRaisesRegexp(CommandParsingError, 'The destination cannot be empty'):
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_wav('/some/path/to/song.wav', '')

    @mock.patch('os.walk')
    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__wav_files_are_returned_in_arbitrary_order__source_and_destination_are_ordered_correctly(self, isfile_mock, exists_mock, walk_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = False
        walk_mock.return_value = [
            ('/some/path/to/wavs', (), ('02 - Track 2.wav', '01 - Track 1.wav', '04 - Track 4.wav', '03 - Track 3.wav'))
        ]
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_wav('/some/path/to/wavs', '/some/destination/')
        self.assertEqual(4, len(commands))
        self.assertEqual(commands[0].source, '/some/path/to/wavs/01 - Track 1.wav')
        self.assertEqual(commands[0].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[1].source, '/some/path/to/wavs/02 - Track 2.wav')
        self.assertEqual(commands[1].destination, '/some/destination/02 - Track 2.mp3')
        self.assertEqual(commands[2].source, '/some/path/to/wavs/03 - Track 3.wav')
        self.assertEqual(commands[2].destination, '/some/destination/03 - Track 3.mp3')
        self.assertEqual(commands[3].source, '/some/path/to/wavs/04 - Track 4.wav')
        self.assertEqual(commands[3].destination, '/some/destination/04 - Track 4.mp3')

    @mock.patch('os.path.exists')
    @mock.patch('os.path.isfile')
    def test__parse_wav__source_is_file_but_destination_is_directory__throws_command_parsing_error(self, isfile_mock, exists_mock):
        exists_mock.return_value = True
        isfile_mock.return_value = True
        with self.assertRaisesRegexp(CommandParsingError, 'If the source is a file, the destination must also be a file.'):
            config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_wav('/some/path/to/song.wav', '/some/destination/')

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    def test__parse_cd_rip__cd_has_5_tracks__it_should_generate_a_correctly_specified_rip_cd_command_and_5_correctly_specified_encode_wav_to_mp3_commands(self, number_of_tracks_mock):
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        number_of_tracks_mock.return_value = 5
        commands = parser.parse_cd_rip('/tmp/rip/destination', '/some/destination')
        self.assertEqual(6, len(commands))
        self.assertIsInstance(commands[0], RipCdCommand)
        self.assertEqual(commands[0].destination, '/tmp/rip/destination')
        self.assertIsInstance(commands[1], EncodeWavCommand)
        self.assertEqual(commands[1].source, '/tmp/rip/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].destination, '/some/destination/01 - Track 1.mp3')
        self.assertIsInstance(commands[2], EncodeWavCommand)
        self.assertEqual(commands[2].source, '/tmp/rip/destination/02 - Track 2.wav')
        self.assertEqual(commands[2].destination, '/some/destination/02 - Track 2.mp3')
        self.assertIsInstance(commands[3], EncodeWavCommand)
        self.assertEqual(commands[3].source, '/tmp/rip/destination/03 - Track 3.wav')
        self.assertEqual(commands[3].destination, '/some/destination/03 - Track 3.mp3')
        self.assertIsInstance(commands[4], EncodeWavCommand)
        self.assertEqual(commands[4].source, '/tmp/rip/destination/04 - Track 4.wav')
        self.assertEqual(commands[4].destination, '/some/destination/04 - Track 4.mp3')
        self.assertIsInstance(commands[5], EncodeWavCommand)
        self.assertEqual(commands[5].source, '/tmp/rip/destination/05 - Track 5.wav')
        self.assertEqual(commands[5].destination, '/some/destination/05 - Track 5.mp3')

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    def test__parse_cd_rip__cd_has_12_tracks__the_track_numbers_should_be_padded_correctly(self, number_of_tracks_mock):
        config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
        number_of_tracks_mock.return_value = 12
        parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
        commands = parser.parse_cd_rip('/tmp/rip/destination', '/some/destination')
        self.assertEqual(13, len(commands))
        self.assertEqual(commands[1].source, '/tmp/rip/destination/01 - Track 1.wav')
        self.assertEqual(commands[1].destination, '/some/destination/01 - Track 1.mp3')
        self.assertEqual(commands[10].source, '/tmp/rip/destination/10 - Track 10.wav')
        self.assertEqual(commands[10].destination, '/some/destination/10 - Track 10.mp3')

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    def test__parse_cd_rip__rip_destination_is_empty__throws_command_parsing_exception(self, number_of_tracks_mock):
        with self.assertRaisesRegexp(CommandParsingError, 'The rip destination cannot be empty'):
            number_of_tracks_mock.return_value = 5
            config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_cd_rip('', '/some/destination')

    @mock.patch('amu.utils.get_number_of_tracks_on_cd')
    def test__parse_cd_rip__destination_is_empty__throws_command_parsing_exception(self, number_of_tracks_mock):
        with self.assertRaisesRegexp(CommandParsingError, 'The destination cannot be empty'):
            number_of_tracks_mock.return_value = 5
            config_mock, cd_ripper_mock, encoder_mock = (Mock(),)*3
            parser = EncodeCommandParser(config_mock, cd_ripper_mock, encoder_mock)
            parser.parse_cd_rip('/tmp/rip/destination', '')
