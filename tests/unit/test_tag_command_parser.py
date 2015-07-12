import mock
import unittest
from amu.commands import AddMp3TagCommand
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
        command_args.year = '2001'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('2001', commands[0].year)

    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__genre_is_specified__add_mp3_tag_command_has_genre_correctly_specified(self, config_mock, isfile_mock):
        isfile_mock.return_value = True
        command_args = AddTagCommandArgs()
        command_args.source = '/some/path/to/song.mp3'
        command_args.artist = 'Aphex Twin'
        command_args.album = 'Druqks'
        command_args.title = 'Vordhosbn'
        command_args.year = '2001'
        command_args.genre = 'Electronic'
        parser = TagCommandParser(config_mock)
        commands = parser.parse_add_mp3_tag_command(command_args)
        self.assertEqual('Electronic', commands[0].genre)

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

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_source(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
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

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_track_numbers(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
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

    @mock.patch('os.walk')
    @mock.patch('os.path.isfile')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_add_mp3_tag_command__source_is_multi_cd_directory__returns_8_add_mp3_tag_commands_with_correct_track_totals(self, config_mock, isfile_mock, walk_mock):
        walk_mock.return_value = [
            ('/some/path/to/mp3s', ('cd1', 'cd2'), ()),
            ('/some/path/to/mp3s/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3')),
            ('/some/path/to/mp3s/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3'))
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