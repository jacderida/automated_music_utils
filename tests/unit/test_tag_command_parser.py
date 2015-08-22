import mock
import unittest
from amu.commands import AddMp3TagCommand
from amu.models import ReleaseModel
from amu.parsing import AddTagCommandArgs
from amu.parsing import CommandParsingError
from amu.parsing import TagCommandParser


class TagCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file__returns_single_add_mp3_tag_command(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(1, len(commands))
        self.assertIsInstance(commands[0], AddMp3TagCommand)
        self.assertEqual('/some/path/to/song.mp3', commands[0].source)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__artist_is_specified__add_mp3_tag_command_has_artist_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Aphex Twin', commands[0].artist)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__album_is_specified__add_mp3_tag_command_has_album_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Druqks', commands[0].album)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__title_is_specified__add_mp3_tag_command_has_title_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Vordhosbn', commands[0].title)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__year_is_specified__add_mp3_tag_command_has_year_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.year = 2001
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(2001, commands[0].year)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__genre_is_specified__add_mp3_tag_command_has_genre_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.year = 2001
        command_args.genre = 'Electronic'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Electronic', commands[0].genre)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__comment_is_specified__add_mp3_tag_command_has_comment_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.year = 2001
        command_args.genre = 'Electronic'
        command_args.comment = 'Warp Records (WARPCD92)'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Warp Records (WARPCD92)', commands[0].comment)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_no_track_number_is_specified__add_mp3_tag_command_has_track_number_set_to_1(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(1, commands[0].track_number)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_no_track_number_is_specified__add_mp3_tag_command_has_track_total_set_to_1(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(1, commands[0].track_total)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_track_number_is_specified__add_mp3_tag_command_has_track_number_set(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.track_number = 2
        command_args.track_total = 10
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(2, commands[0].track_number)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_track_total_is_specified__add_mp3_tag_command_has_track_total_set(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.track_number = 2
        command_args.track_total = 10
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(10, commands[0].track_total)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_file_and_track_number_is_specified_but_track_total_is_not__command_parsing_error_is_raised(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.track_number = 2
        parser = TagCommandParser(config_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'If a track number has been supplied, a track total must also be supplied.'):
            parser.parse_add_mp3_tag_command(command_args)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_4_mp3s__returns_4_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(4, len(commands))
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__walk_returns_files_in_arbitrary_order__returns_4_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('04 - Track 4.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '01 - Track 1.mp3'))
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(4, len(commands))
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_4_mp3s__returns_4_add_mp3_tag_commands_with_correct_track_numbers(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(4, len(commands))
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_4_mp3s__returns_4_add_mp3_tag_commands_with_correct_track_totals(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(4, len(commands))
        self.assertEqual(4, commands[0].track_total)
        self.assertEqual(4, commands[1].track_total)
        self.assertEqual(4, commands[2].track_total)
        self.assertEqual(4, commands[3].track_total)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_directory_with_track_number_override__command_parsing_error_is_raised(self, config_mock, isfile_mock):
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.track_number = 2
        command_args.track_total = 10
        parser = TagCommandParser(config_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'With a directory source, a track number and total override cannot be specified.'):
            parser.parse_add_mp3_tag_command(command_args)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock, listdir_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3']
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(8, len(commands))
        self.assertEqual('/some/path/to/mp3s/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/cd1/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/cd1/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/cd1/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/cd2/01 - Track 1.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/cd2/02 - Track 2.mp3', commands[5].source)
        self.assertEqual('/some/path/to/mp3s/cd2/03 - Track 3.mp3', commands[6].source)
        self.assertEqual('/some/path/to/mp3s/cd2/04 - Track 4.mp3', commands[7].source)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory_and_walk_returns_directories_in_arbitrary_order__returns_16_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock, listdir_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd4', 'cd2', 'cd3', 'cd1'), ()),
            ('/some/path/to/mp3s/cd4', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd3', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3']
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(16, len(commands))
        self.assertEqual('/some/path/to/mp3s/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/cd1/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/cd1/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/cd1/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/cd2/01 - Track 1.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/cd2/02 - Track 2.mp3', commands[5].source)
        self.assertEqual('/some/path/to/mp3s/cd2/03 - Track 3.mp3', commands[6].source)
        self.assertEqual('/some/path/to/mp3s/cd2/04 - Track 4.mp3', commands[7].source)
        self.assertEqual('/some/path/to/mp3s/cd3/01 - Track 1.mp3', commands[8].source)
        self.assertEqual('/some/path/to/mp3s/cd3/02 - Track 2.mp3', commands[9].source)
        self.assertEqual('/some/path/to/mp3s/cd3/03 - Track 3.mp3', commands[10].source)
        self.assertEqual('/some/path/to/mp3s/cd3/04 - Track 4.mp3', commands[11].source)
        self.assertEqual('/some/path/to/mp3s/cd4/01 - Track 1.mp3', commands[12].source)
        self.assertEqual('/some/path/to/mp3s/cd4/02 - Track 2.mp3', commands[13].source)
        self.assertEqual('/some/path/to/mp3s/cd4/03 - Track 3.mp3', commands[14].source)
        self.assertEqual('/some/path/to/mp3s/cd4/04 - Track 4.mp3', commands[15].source)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_track_numbers(self, config_mock, isfile_mock, walk_mock, listdir_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3']
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(8, len(commands))
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)
        self.assertEqual(1, commands[4].track_number)
        self.assertEqual(2, commands[5].track_number)
        self.assertEqual(3, commands[6].track_number)
        self.assertEqual(4, commands[7].track_number)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_track_totals(self, config_mock, isfile_mock, walk_mock, listdir_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3'))
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3']
        ]
        isfile_mock.return_value = False
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/mp3s'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual(9, len(commands))
        self.assertEqual(4, commands[0].track_total)
        self.assertEqual(4, commands[1].track_total)
        self.assertEqual(4, commands[2].track_total)
        self.assertEqual(4, commands[3].track_total)
        self.assertEqual(5, commands[4].track_total)
        self.assertEqual(5, commands[5].track_total)
        self.assertEqual(5, commands[6].track_total)
        self.assertEqual(5, commands[7].track_total)
        self.assertEqual(5, commands[8].track_total)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__6_add_mp3_tag_commands_are_returned(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(6, len(commands))

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__release_artist_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Legowelt', commands[0].artist)
        self.assertEqual('Legowelt', commands[1].artist)
        self.assertEqual('Legowelt', commands[2].artist)
        self.assertEqual('Legowelt', commands[3].artist)
        self.assertEqual('Legowelt', commands[4].artist)
        self.assertEqual('Legowelt', commands[5].artist)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__release_album_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Pimpshifter', commands[0].album)
        self.assertEqual('Pimpshifter', commands[1].album)
        self.assertEqual('Pimpshifter', commands[2].album)
        self.assertEqual('Pimpshifter', commands[3].album)
        self.assertEqual('Pimpshifter', commands[4].album)
        self.assertEqual('Pimpshifter', commands[5].album)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__title_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Sturmvogel', commands[0].title)
        self.assertEqual('Geneva Hideout', commands[1].title)
        self.assertEqual('Ricky Ramjet', commands[2].title)
        self.assertEqual('Nuisance Lover', commands[3].title)
        self.assertEqual('Strange Girl', commands[4].title)
        self.assertEqual('Total Pussy Control', commands[5].title)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__genre_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Electronic', commands[0].genre)
        self.assertEqual('Electronic', commands[1].genre)
        self.assertEqual('Electronic', commands[2].genre)
        self.assertEqual('Electronic', commands[3].genre)
        self.assertEqual('Electronic', commands[4].genre)
        self.assertEqual('Electronic', commands[5].genre)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__year_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(2000, commands[0].year)
        self.assertEqual(2000, commands[1].year)
        self.assertEqual(2000, commands[2].year)
        self.assertEqual(2000, commands[3].year)
        self.assertEqual(2000, commands[4].year)
        self.assertEqual(2000, commands[5].year)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__track_number_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)
        self.assertEqual(5, commands[4].track_number)
        self.assertEqual(6, commands[5].track_number)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__track_total_is_set_on_tracks(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(6, commands[0].track_total)
        self.assertEqual(6, commands[1].track_total)
        self.assertEqual(6, commands[2].track_total)
        self.assertEqual(6, commands[3].track_total)
        self.assertEqual(6, commands[4].track_total)
        self.assertEqual(6, commands[5].track_total)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_single_artist_and_6_tracks__source_is_set_correctly(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/06 - Track 6.mp3', commands[5].source)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__walk_returns_tracks_in_arbitrary_order__sources_are_specified_in_correct_order(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('05 - Track 5.mp3', '02 - Track 2.mp3', '04 - Track 4.mp3', '01 - Track 1.mp3', '03 - Track 3.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('/some/path/to/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/06 - Track 6.mp3', commands[5].source)

    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_has_artists_on_tracks__artists_are_set_correctly(self, config_mock, walk_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3')),
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Legowelt', commands[0].artist)
        self.assertEqual('It & My Computer', commands[1].artist)
        self.assertEqual('Orgue Electronique', commands[2].artist)
        self.assertEqual('Luke Eargoggle', commands[3].artist)
        self.assertEqual('Porn.Darsteller', commands[4].artist)
        self.assertEqual('Sendex', commands[5].artist)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__24_add_mp3_tag_commands_are_returned(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works Volume II'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD21'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '1994'
        release_model.genre = 'Electronic'
        release_model.style = 'Experimental, Ambient'
        release_model.add_track_directly(None, 'Untitled', 1, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 1, 2)
        release_model.add_track_directly(None, 'Blue Calx', 1, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(24, len(commands))

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__source_is_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works Volume II'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD21'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '1994'
        release_model.genre = 'Electronic'
        release_model.style = 'Experimental, Ambient'
        release_model.add_track_directly(None, 'Untitled', 1, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 1, 2)
        release_model.add_track_directly(None, 'Blue Calx', 1, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('/some/path/to/mp3s/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/cd1/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/cd1/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/cd1/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/cd1/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/cd1/06 - Track 6.mp3', commands[5].source)
        self.assertEqual('/some/path/to/mp3s/cd1/07 - Track 7.mp3', commands[6].source)
        self.assertEqual('/some/path/to/mp3s/cd1/08 - Track 8.mp3', commands[7].source)
        self.assertEqual('/some/path/to/mp3s/cd1/09 - Track 9.mp3', commands[8].source)
        self.assertEqual('/some/path/to/mp3s/cd1/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/path/to/mp3s/cd1/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/path/to/mp3s/cd1/12 - Track 12.mp3', commands[11].source)
        self.assertEqual('/some/path/to/mp3s/cd2/01 - Track 1.mp3', commands[12].source)
        self.assertEqual('/some/path/to/mp3s/cd2/02 - Track 2.mp3', commands[13].source)
        self.assertEqual('/some/path/to/mp3s/cd2/03 - Track 3.mp3', commands[14].source)
        self.assertEqual('/some/path/to/mp3s/cd2/04 - Track 4.mp3', commands[15].source)
        self.assertEqual('/some/path/to/mp3s/cd2/05 - Track 5.mp3', commands[16].source)
        self.assertEqual('/some/path/to/mp3s/cd2/06 - Track 6.mp3', commands[17].source)
        self.assertEqual('/some/path/to/mp3s/cd2/07 - Track 7.mp3', commands[18].source)
        self.assertEqual('/some/path/to/mp3s/cd2/08 - Track 8.mp3', commands[19].source)
        self.assertEqual('/some/path/to/mp3s/cd2/09 - Track 9.mp3', commands[20].source)
        self.assertEqual('/some/path/to/mp3s/cd2/10 - Track 10.mp3', commands[21].source)
        self.assertEqual('/some/path/to/mp3s/cd2/11 - Track 11.mp3', commands[22].source)
        self.assertEqual('/some/path/to/mp3s/cd2/12 - Track 12.mp3', commands[23].source)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd_and_walk_returns_directories_in_arbitrary_order__source_is_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Acid Mothers Temple & The Melting Paraiso UFO'
        release_model.title = 'The Penultimate Galactic Bordello Also The World You Made'
        release_model.label = 'Dirter Promotions'
        release_model.catno = 'DPROMCD53'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 4
        release_model.country = 'UK'
        release_model.year = '2004'
        release_model.genre = 'Rock'
        release_model.style = 'Psychedelic Rock, Experimental'
        release_model.add_track_directly(None, 'The Beautiful Blue Ecstasy (Have You Seen The Blue Sky?)', 1, 1, 1, 4)
        release_model.add_track_directly(None, 'The Seven Stigmata From Pussycat Nebula', 1, 1, 2, 4)
        release_model.add_track_directly(None, "What's Your Name?", 1, 1, 3, 4)
        release_model.add_track_directly(None, 'The Holly Mountain In The Counter-Clock World', 1, 1, 4, 4)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd4', 'cd2', 'cd1', 'cd3'), ()),
            (source_path + '/cd4', (), ('01 - Track 1.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3')),
            (source_path + '/cd1', (), ('01 - Track 1.mp3')),
            (source_path + '/cd3', (), ('01 - Track 1.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3'],
            ['01 - Track 1.mp3'],
            ['01 - Track 1.mp3'],
            ['01 - Track 1.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('/some/path/to/mp3s/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/cd2/01 - Track 1.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/cd3/01 - Track 1.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/cd4/01 - Track 1.mp3', commands[3].source)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__titles_are_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '26 Mixes For Cash'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD102'
        release_model.format = 'CD, Compilation'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '2003'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Drum n Bass, Ambient, Experimental, Acid'
        release_model.add_track_directly('Seefeel', 'Time To Find Me (AFX Fast Mix)', 1, 13, 1, 2)
        release_model.add_track_directly('Gavin Bryars', 'Raising The Titanic (Big Drum Mix)', 2, 13, 1, 2)
        release_model.add_track_directly('Gentle People', 'Journey (Aphex Twin Care Mix)', 3, 13, 1, 2)
        release_model.add_track_directly('Kinesthesia', 'Triachus (Mix By Aphex Twin)', 4, 13, 1, 2)
        release_model.add_track_directly('Phillip Glass', 'Hereos (Aphex Twin Remix)', 5, 13, 1, 2)
        release_model.add_track_directly('Buck Tick', 'In The Glitter Part 2 (Aphex Twin Mix)', 6, 13, 1, 2)
        release_model.add_track_directly('Jesus Jones', 'Zeros And Ones (Aphex Twin Reconstruction #2)', 7, 13, 1, 2)
        release_model.add_track_directly('Nav Katze', 'Ziggy (Aphex Twin Mix #1)', 8, 13, 1, 2)
        release_model.add_track_directly('Saint Etienne', 'Your Head My Voice (Voix Revirement)', 9, 13, 1, 2)
        release_model.add_track_directly('Nav Katze', 'Change (Aphex Twin Mix #1)', 10, 13, 1, 2)
        release_model.add_track_directly('Beatniks, The', "Une Femme N'est Pas Un Homme (Aphex Twin Mix)", 11, 13, 1, 2)
        release_model.add_track_directly('Nine Inch Nails', 'The Beauty Of Being Numb Section B (Created By Aphex Twin)', 12, 13, 1, 2)
        release_model.add_track_directly('Nobukazu Takemura', 'Let My Fish Loose (Aphex Twin Remix)', 12, 13, 1, 2)
        release_model.add_track_directly('Die Fantastischen Vier', 'Kreiger (Aphex Twin Baldhu Mix)', 1, 13, 2, 2)
        release_model.add_track_directly('Phillip Boa & The Voodoo Club', 'Deep In Velvet (Aphex Twin Turnips Mix)', 2, 13, 2, 2)
        release_model.add_track_directly('Curve', 'Falling Free (Aphex Twin Remix)', 3, 13, 2, 2)
        release_model.add_track_directly('Mescalinum United', 'We Have Arrived (Aphex Twin QQT Mix)', 4, 13, 2, 2)
        release_model.add_track_directly('Nine Inch Nails', 'At The Heart Of It All (Created By Aphex Twin)', 5, 13, 2, 2)
        release_model.add_track_directly('808 State', 'Flow Coma (Remix By AFX)', 6, 13, 2, 2)
        release_model.add_track_directly('Aphex Twin', 'Window Licker (Acid Edit)', 7, 13, 2, 2)
        release_model.add_track_directly('Baby Ford', 'Normal (Helston Flora Remix By AFX)', 8, 13, 2, 2)
        release_model.add_track_directly('Aphex Twin', 'SAW2 CD1 TRK2 (Original Mix)', 9, 13, 2, 2)
        release_model.add_track_directly('Meat Beat Manifesto', 'Mindstream (The Aphex Twin Remix)', 10, 13, 2, 2)
        release_model.add_track_directly('DMX Krew', "You Can't Hide Your Love (Hidden Love Mix)", 11, 13, 2, 2)
        release_model.add_track_directly('Wagon Christ', 'Spotlight (Aphex Twin Mix)', 12, 13, 2, 2)
        release_model.add_track_directly('Mike Flowers Pops', 'Debase (Soft Palate)', 13, 13, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Time To Find Me (AFX Fast Mix)', commands[0].title)
        self.assertEqual('Raising The Titanic (Big Drum Mix)', commands[1].title)
        self.assertEqual('Journey (Aphex Twin Care Mix)', commands[2].title)
        self.assertEqual('Triachus (Mix By Aphex Twin)', commands[3].title)
        self.assertEqual('Hereos (Aphex Twin Remix)', commands[4].title)
        self.assertEqual('In The Glitter Part 2 (Aphex Twin Mix)', commands[5].title)
        self.assertEqual('Zeros And Ones (Aphex Twin Reconstruction #2)', commands[6].title)
        self.assertEqual('Ziggy (Aphex Twin Mix #1)', commands[7].title)
        self.assertEqual('Your Head My Voice (Voix Revirement)', commands[8].title)
        self.assertEqual('Change (Aphex Twin Mix #1)', commands[9].title)
        self.assertEqual("Une Femme N'est Pas Un Homme (Aphex Twin Mix)", commands[10].title)
        self.assertEqual('The Beauty Of Being Numb Section B (Created By Aphex Twin)', commands[11].title)
        self.assertEqual('Let My Fish Loose (Aphex Twin Remix)', commands[12].title)
        self.assertEqual('Kreiger (Aphex Twin Baldhu Mix)', commands[13].title)
        self.assertEqual('Deep In Velvet (Aphex Twin Turnips Mix)', commands[14].title)
        self.assertEqual('Falling Free (Aphex Twin Remix)', commands[15].title)
        self.assertEqual('We Have Arrived (Aphex Twin QQT Mix)', commands[16].title)
        self.assertEqual('At The Heart Of It All (Created By Aphex Twin)', commands[17].title)
        self.assertEqual('Flow Coma (Remix By AFX)', commands[18].title)
        self.assertEqual('Window Licker (Acid Edit)', commands[19].title)
        self.assertEqual('Normal (Helston Flora Remix By AFX)', commands[20].title)
        self.assertEqual('SAW2 CD1 TRK2 (Original Mix)', commands[21].title)
        self.assertEqual('Mindstream (The Aphex Twin Remix)', commands[22].title)
        self.assertEqual("You Can't Hide Your Love (Hidden Love Mix)", commands[23].title)
        self.assertEqual('Spotlight (Aphex Twin Mix)', commands[24].title)
        self.assertEqual('Debase (Soft Palate)', commands[25].title)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__artists_are_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = '26 Mixes For Cash'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD102'
        release_model.format = 'CD, Compilation'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '2003'
        release_model.genre = 'Electronic'
        release_model.style = 'IDM, Drum n Bass, Ambient, Experimental, Acid'
        release_model.add_track_directly('Seefeel', 'Time To Find Me (AFX Fast Mix)', 1, 13, 1, 2)
        release_model.add_track_directly('Gavin Bryars', 'Raising The Titanic (Big Drum Mix)', 2, 13, 1, 2)
        release_model.add_track_directly('Gentle People', 'Journey (Aphex Twin Care Mix)', 3, 13, 1, 2)
        release_model.add_track_directly('Kinesthesia', 'Triachus (Mix By Aphex Twin)', 4, 13, 1, 2)
        release_model.add_track_directly('Phillip Glass', 'Hereos (Aphex Twin Remix)', 5, 13, 1, 2)
        release_model.add_track_directly('Buck Tick', 'In The Glitter Part 2 (Aphex Twin Mix)', 6, 13, 1, 2)
        release_model.add_track_directly('Jesus Jones', 'Zeros And Ones (Aphex Twin Reconstruction #2)', 7, 13, 1, 2)
        release_model.add_track_directly('Nav Katze', 'Ziggy (Aphex Twin Mix #1)', 8, 13, 1, 2)
        release_model.add_track_directly('Saint Etienne', 'Your Head My Voice (Voix Revirement)', 9, 13, 1, 2)
        release_model.add_track_directly('Nav Katze', 'Change (Aphex Twin Mix #1)', 10, 13, 1, 2)
        release_model.add_track_directly('Beatniks, The', "Une Femme N'est Pas Un Homme (Aphex Twin Mix)", 11, 13, 1, 2)
        release_model.add_track_directly('Nine Inch Nails', 'The Beauty Of Being Numb Section B (Created By Aphex Twin)', 12, 13, 1, 2)
        release_model.add_track_directly('Nobukazu Takemura', 'Let My Fish Loose (Aphex Twin Remix)', 12, 13, 1, 2)
        release_model.add_track_directly('Die Fantastischen Vier', 'Kreiger (Aphex Twin Baldhu Mix)', 1, 13, 2, 2)
        release_model.add_track_directly('Phillip Boa & The Voodoo Club', 'Deep In Velvet (Aphex Twin Turnips Mix)', 2, 13, 2, 2)
        release_model.add_track_directly('Curve', 'Falling Free (Aphex Twin Remix)', 3, 13, 2, 2)
        release_model.add_track_directly('Mescalinum United', 'We Have Arrived (Aphex Twin QQT Mix)', 4, 13, 2, 2)
        release_model.add_track_directly('Nine Inch Nails', 'At The Heart Of It All (Created By Aphex Twin)', 5, 13, 2, 2)
        release_model.add_track_directly('808 State', 'Flow Coma (Remix By AFX)', 6, 13, 2, 2)
        release_model.add_track_directly('Aphex Twin', 'Window Licker (Acid Edit)', 7, 13, 2, 2)
        release_model.add_track_directly('Baby Ford', 'Normal (Helston Flora Remix By AFX)', 8, 13, 2, 2)
        release_model.add_track_directly('Aphex Twin', 'SAW2 CD1 TRK2 (Original Mix)', 9, 13, 2, 2)
        release_model.add_track_directly('Meat Beat Manifesto', 'Mindstream (The Aphex Twin Remix)', 10, 13, 2, 2)
        release_model.add_track_directly('DMX Krew', "You Can't Hide Your Love (Hidden Love Mix)", 11, 13, 2, 2)
        release_model.add_track_directly('Wagon Christ', 'Spotlight (Aphex Twin Mix)', 12, 13, 2, 2)
        release_model.add_track_directly('Mike Flowers Pops', 'Debase (Soft Palate)', 13, 13, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual('Seefeel', commands[0].artist)
        self.assertEqual('Gavin Bryars', commands[1].artist)
        self.assertEqual('Gentle People', commands[2].artist)
        self.assertEqual('Kinesthesia', commands[3].artist)
        self.assertEqual('Phillip Glass', commands[4].artist)
        self.assertEqual('Buck Tick', commands[5].artist)
        self.assertEqual('Jesus Jones', commands[6].artist)
        self.assertEqual('Nav Katze', commands[7].artist)
        self.assertEqual('Saint Etienne', commands[8].artist)
        self.assertEqual('Nav Katze', commands[9].artist)
        self.assertEqual('Beatniks, The', commands[10].artist)
        self.assertEqual('Nine Inch Nails', commands[11].artist)
        self.assertEqual('Nobukazu Takemura', commands[12].artist)
        self.assertEqual('Die Fantastischen Vier', commands[13].artist)
        self.assertEqual('Phillip Boa & The Voodoo Club', commands[14].artist)
        self.assertEqual('Curve', commands[15].artist)
        self.assertEqual('Mescalinum United', commands[16].artist)
        self.assertEqual('Nine Inch Nails', commands[17].artist)
        self.assertEqual('808 State', commands[18].artist)
        self.assertEqual('Aphex Twin', commands[19].artist)
        self.assertEqual('Baby Ford', commands[20].artist)
        self.assertEqual('Aphex Twin', commands[21].artist)
        self.assertEqual('Meat Beat Manifesto', commands[22].artist)
        self.assertEqual('DMX Krew', commands[23].artist)
        self.assertEqual('Wagon Christ', commands[24].artist)
        self.assertEqual('Mike Flowers Pops', commands[25].artist)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__track_numbers_are_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works Volume II'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD21'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '1994'
        release_model.genre = 'Electronic'
        release_model.style = 'Experimental, Ambient'
        release_model.add_track_directly(None, 'Untitled', 1, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 1, 2)
        release_model.add_track_directly(None, 'Blue Calx', 1, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)
        self.assertEqual(5, commands[4].track_number)
        self.assertEqual(6, commands[5].track_number)
        self.assertEqual(7, commands[6].track_number)
        self.assertEqual(8, commands[7].track_number)
        self.assertEqual(9, commands[8].track_number)
        self.assertEqual(10, commands[9].track_number)
        self.assertEqual(11, commands[10].track_number)
        self.assertEqual(12, commands[11].track_number)
        self.assertEqual(1, commands[12].track_number)
        self.assertEqual(2, commands[13].track_number)
        self.assertEqual(3, commands[14].track_number)
        self.assertEqual(4, commands[15].track_number)
        self.assertEqual(5, commands[16].track_number)
        self.assertEqual(6, commands[17].track_number)
        self.assertEqual(7, commands[18].track_number)
        self.assertEqual(8, commands[19].track_number)
        self.assertEqual(9, commands[20].track_number)
        self.assertEqual(10, commands[21].track_number)
        self.assertEqual(11, commands[22].track_number)
        self.assertEqual(12, commands[23].track_number)

    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model__release_is_multi_cd__track_totals_are_set_correctly(self, config_mock, walk_mock, listdir_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works Volume II'
        release_model.label = 'Warp Records'
        release_model.catno = 'WARPCD21'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 2
        release_model.country = 'UK'
        release_model.year = '1994'
        release_model.genre = 'Electronic'
        release_model.style = 'Experimental, Ambient'
        release_model.add_track_directly(None, 'Untitled', 1, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 1, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 1, 2)
        release_model.add_track_directly(None, 'Blue Calx', 1, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 2, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 3, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 4, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 5, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 6, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 7, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 8, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 9, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 10, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 11, 12, 2, 2)
        release_model.add_track_directly(None, 'Untitled', 12, 12, 2, 2)
        source_path = '/some/path/to/mp3s'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3']
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, release_model)
        self.assertEqual(12, commands[0].track_total)
        self.assertEqual(12, commands[1].track_total)
        self.assertEqual(12, commands[2].track_total)
        self.assertEqual(12, commands[3].track_total)
        self.assertEqual(12, commands[4].track_total)
        self.assertEqual(12, commands[5].track_total)
        self.assertEqual(12, commands[6].track_total)
        self.assertEqual(12, commands[7].track_total)
        self.assertEqual(12, commands[8].track_total)
        self.assertEqual(12, commands[9].track_total)
        self.assertEqual(12, commands[10].track_total)
        self.assertEqual(12, commands[11].track_total)
        self.assertEqual(12, commands[12].track_total)
        self.assertEqual(12, commands[13].track_total)
        self.assertEqual(12, commands[14].track_total)
        self.assertEqual(12, commands[15].track_total)
        self.assertEqual(12, commands[16].track_total)
        self.assertEqual(12, commands[17].track_total)
        self.assertEqual(12, commands[18].track_total)
        self.assertEqual(12, commands[19].track_total)
        self.assertEqual(12, commands[20].track_total)
        self.assertEqual(12, commands[21].track_total)
        self.assertEqual(12, commands[22].track_total)
        self.assertEqual(12, commands[23].track_total)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__4_add_tag_commands_are_generated(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual(4, len(commands))

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__sources_are_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('/some/source/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/mp3s/04 - Track 4.mp3', commands[3].source)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_13_tracks__sources_are_specified_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works 85-92'
        release_model.label = 'Apollo'
        release_model.catno = 'AMB 3922 CD'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1992'
        release_model.genre = 'Electronic'
        release_model.style = 'Techno, IDM, Ambient'
        release_model.add_track_directly(None, 'Xtal', 1, 13, 1, 1)
        release_model.add_track_directly(None, 'Tha', 2, 13, 1, 1)
        release_model.add_track_directly(None, 'Pulsewidth', 3, 13, 1, 1)
        release_model.add_track_directly(None, 'Ageispolis', 4, 13, 1, 1)
        release_model.add_track_directly(None, 'I', 5, 13, 1, 1)
        release_model.add_track_directly(None, 'Green Calx', 6, 13, 1, 1)
        release_model.add_track_directly(None, 'Heliosphan', 7, 13, 1, 1)
        release_model.add_track_directly(None, 'We Are The Music Makers', 8, 13, 1, 1)
        release_model.add_track_directly(None, 'Schottkey 7th Path', 9, 13, 1, 1)
        release_model.add_track_directly(None, 'Ptolemy', 10, 13, 1, 1)
        release_model.add_track_directly(None, 'Hedphelym', 11, 13, 1, 1)
        release_model.add_track_directly(None, 'Delphium', 12, 13, 1, 1)
        release_model.add_track_directly(None, 'Actium', 13, 13, 1, 1)

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('/some/source/mp3s/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/mp3s/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/mp3s/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/mp3s/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/source/mp3s/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/source/mp3s/06 - Track 6.mp3', commands[5].source)
        self.assertEqual('/some/source/mp3s/07 - Track 7.mp3', commands[6].source)
        self.assertEqual('/some/source/mp3s/08 - Track 8.mp3', commands[7].source)
        self.assertEqual('/some/source/mp3s/09 - Track 9.mp3', commands[8].source)
        self.assertEqual('/some/source/mp3s/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/source/mp3s/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/source/mp3s/12 - Track 12.mp3', commands[11].source)
        self.assertEqual('/some/source/mp3s/13 - Track 13.mp3', commands[12].source)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__artists_are_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('AFX', commands[0].artist)
        self.assertEqual('AFX', commands[1].artist)
        self.assertEqual('AFX', commands[2].artist)
        self.assertEqual('AFX', commands[3].artist)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__titles_are_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('PWSteal.Ldpinch.D', commands[0].title)
        self.assertEqual('Backdoor.Berbew.Q', commands[1].title)
        self.assertEqual('W32.Deadcode.A', commands[2].title)
        self.assertEqual('Backdoor.Spyboter.A', commands[3].title)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__album_is_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('Analord 08', commands[0].album)
        self.assertEqual('Analord 08', commands[1].album)
        self.assertEqual('Analord 08', commands[2].album)
        self.assertEqual('Analord 08', commands[3].album)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__genre_is_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('Electronic', commands[0].genre)
        self.assertEqual('Electronic', commands[1].genre)
        self.assertEqual('Electronic', commands[2].genre)
        self.assertEqual('Electronic', commands[3].genre)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__track_numbers_are_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__track_totals_are_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual(4, commands[0].track_total)
        self.assertEqual(4, commands[1].track_total)
        self.assertEqual(4, commands[2].track_total)
        self.assertEqual(4, commands[3].track_total)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_4_tracks__year_is_specified_correctly(self, config_mock):
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

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual(2005, commands[0].year)
        self.assertEqual(2005, commands[1].year)
        self.assertEqual(2005, commands[2].year)
        self.assertEqual(2005, commands[3].year)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_empty_source__release_has_artists_on_tracks__artists_are_specified_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_empty_source('/some/source/mp3s', release_model)
        self.assertEqual('Legowelt', commands[0].artist)
        self.assertEqual('It & My Computer', commands[1].artist)
        self.assertEqual('Orgue Electronique', commands[2].artist)
        self.assertEqual('Luke Eargoggle', commands[3].artist)
        self.assertEqual('Porn.Darsteller', commands[4].artist)
        self.assertEqual('Sendex', commands[5].artist)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__6_tag_mp3_commands_are_returned(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual(6, len(commands))

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_and_sources_have_different_lengths__command_parsing_error_is_raise(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3',
            '/some/path/to/mp3s/07 - Track 07.mp3'
        ]

        parser = TagCommandParser(config_mock)
        with self.assertRaisesRegexp(CommandParsingError, 'The source must have the same number of tracks as the release.'):
            parser.parse_from_release_model_with_sources(release_model, sources)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__sources_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual('/some/path/to/mp3s/01 - Track 01.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 02.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 03.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 04.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/05 - Track 05.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/06 - Track 06.mp3', commands[5].source)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_13_tracks__sources_are_specified_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Aphex Twin'
        release_model.title = 'Selected Ambient Works 85-92'
        release_model.label = 'Apollo'
        release_model.catno = 'AMB 3922 CD'
        release_model.format = 'CD, Album'
        release_model.format_quantity = 1
        release_model.country = 'UK'
        release_model.year = '1992'
        release_model.genre = 'Electronic'
        release_model.style = 'Techno, IDM, Ambient'
        release_model.add_track_directly(None, 'Xtal', 1, 13, 1, 1)
        release_model.add_track_directly(None, 'Tha', 2, 13, 1, 1)
        release_model.add_track_directly(None, 'Pulsewidth', 3, 13, 1, 1)
        release_model.add_track_directly(None, 'Ageispolis', 4, 13, 1, 1)
        release_model.add_track_directly(None, 'I', 5, 13, 1, 1)
        release_model.add_track_directly(None, 'Green Calx', 6, 13, 1, 1)
        release_model.add_track_directly(None, 'Heliosphan', 7, 13, 1, 1)
        release_model.add_track_directly(None, 'We Are The Music Makers', 8, 13, 1, 1)
        release_model.add_track_directly(None, 'Schottkey 7th Path', 9, 13, 1, 1)
        release_model.add_track_directly(None, 'Ptolemy', 10, 13, 1, 1)
        release_model.add_track_directly(None, 'Hedphelym', 11, 13, 1, 1)
        release_model.add_track_directly(None, 'Delphium', 12, 13, 1, 1)
        release_model.add_track_directly(None, 'Actium', 13, 13, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3',
            '/some/path/to/mp3s/07 - Track 07.mp3',
            '/some/path/to/mp3s/08 - Track 08.mp3',
            '/some/path/to/mp3s/09 - Track 09.mp3',
            '/some/path/to/mp3s/10 - Track 10.mp3',
            '/some/path/to/mp3s/11 - Track 11.mp3',
            '/some/path/to/mp3s/12 - Track 12.mp3',
            '/some/path/to/mp3s/13 - Track 13.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual('/some/path/to/mp3s/01 - Track 01.mp3', commands[0].source)
        self.assertEqual('/some/path/to/mp3s/02 - Track 02.mp3', commands[1].source)
        self.assertEqual('/some/path/to/mp3s/03 - Track 03.mp3', commands[2].source)
        self.assertEqual('/some/path/to/mp3s/04 - Track 04.mp3', commands[3].source)
        self.assertEqual('/some/path/to/mp3s/05 - Track 05.mp3', commands[4].source)
        self.assertEqual('/some/path/to/mp3s/06 - Track 06.mp3', commands[5].source)
        self.assertEqual('/some/path/to/mp3s/07 - Track 07.mp3', commands[6].source)
        self.assertEqual('/some/path/to/mp3s/08 - Track 08.mp3', commands[7].source)
        self.assertEqual('/some/path/to/mp3s/09 - Track 09.mp3', commands[8].source)
        self.assertEqual('/some/path/to/mp3s/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/path/to/mp3s/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/path/to/mp3s/12 - Track 12.mp3', commands[11].source)
        self.assertEqual('/some/path/to/mp3s/13 - Track 13.mp3', commands[12].source)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__artists_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual('Legowelt', commands[0].artist)
        self.assertEqual('It & My Computer', commands[1].artist)
        self.assertEqual('Orgue Electronique', commands[2].artist)
        self.assertEqual('Luke Eargoggle', commands[3].artist)
        self.assertEqual('Porn.Darsteller', commands[4].artist)
        self.assertEqual('Sendex', commands[5].artist)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__titles_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual('Crystal Cat', commands[0].title)
        self.assertEqual('Bronx On / Bronx Off', commands[1].title)
        self.assertEqual('Beirut Meeting', commands[2].title)
        self.assertEqual('The Mechanic Priest', commands[3].title)
        self.assertEqual("L'ombre Des Heros", commands[4].title)
        self.assertEqual('Raid On Entebbe', commands[5].title)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__genres_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual('Electronic', commands[0].genre)
        self.assertEqual('Electronic', commands[1].genre)
        self.assertEqual('Electronic', commands[2].genre)
        self.assertEqual('Electronic', commands[3].genre)
        self.assertEqual('Electronic', commands[4].genre)
        self.assertEqual('Electronic', commands[5].genre)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__track_numbers_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual(1, commands[0].track_number)
        self.assertEqual(2, commands[1].track_number)
        self.assertEqual(3, commands[2].track_number)
        self.assertEqual(4, commands[3].track_number)
        self.assertEqual(5, commands[4].track_number)
        self.assertEqual(6, commands[5].track_number)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__track_totals_are_set_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual(6, commands[0].track_total)
        self.assertEqual(6, commands[1].track_total)
        self.assertEqual(6, commands[2].track_total)
        self.assertEqual(6, commands[3].track_total)
        self.assertEqual(6, commands[4].track_total)
        self.assertEqual(6, commands[5].track_total)

    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_release_model_with_sources__release_has_6_tracks__year_is_specified_correctly(self, config_mock):
        release_model = ReleaseModel()
        release_model.artist = 'Various'
        release_model.title = 'Bronson Quest'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3047'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2005'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly('Legowelt', 'Crystal Cat', 1, 6, 1, 1)
        release_model.add_track_directly('It & My Computer', 'Bronx On / Bronx Off', 2, 6, 1, 1)
        release_model.add_track_directly('Orgue Electronique', 'Beirut Meeting', 3, 6, 1, 1)
        release_model.add_track_directly('Luke Eargoggle', 'The Mechanic Priest', 4, 6, 1, 1)
        release_model.add_track_directly('Porn.Darsteller', "L'ombre Des Heros", 5, 6, 1, 1)
        release_model.add_track_directly('Sendex', 'Raid On Entebbe', 6, 6, 1, 1)
        sources = [
            '/some/path/to/mp3s/01 - Track 01.mp3',
            '/some/path/to/mp3s/02 - Track 02.mp3',
            '/some/path/to/mp3s/03 - Track 03.mp3',
            '/some/path/to/mp3s/04 - Track 04.mp3',
            '/some/path/to/mp3s/05 - Track 05.mp3',
            '/some/path/to/mp3s/06 - Track 06.mp3'
        ]

        parser = TagCommandParser(config_mock)
        commands = parser.parse_from_release_model_with_sources(release_model, sources)
        self.assertEqual(2005, commands[0].year)
        self.assertEqual(2005, commands[1].year)
        self.assertEqual(2005, commands[2].year)
        self.assertEqual(2005, commands[3].year)
        self.assertEqual(2005, commands[4].year)
        self.assertEqual(2005, commands[5].year)
