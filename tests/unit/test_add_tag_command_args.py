""" Test suite for the add tags command args class. """
import unittest
from amu.clidriver import CliDriver
from amu.parsing import AddTagCommandArgs


class AddTagCommandArgsTest(unittest.TestCase):
    def test__from_args__when_passed_args_for_add_tag_command__the_source_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('/some/path/to/song.mp3', command_args.source)

    def test__from_args__when_source_has_spaces__the_source_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source="/some/path/with a space/to/song.mp3"',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('/some/path/with a space/to/song.mp3', command_args.source)

    def test__from_args__when_source_is_not_specified__the_source_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.source)

    def test__from_args__when_passed_args_for_add_tag_command__the_artist_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Legowelt', command_args.artist)

    def test__from_args__when_the_artist_has_a_space_in_the_name__the_artist_should_be_specified_without_surrounding_quotes(self):
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
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Aphex Twin', command_args.artist)

    def test__from_args__when_the_artist_is_not_specified__the_artist_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.artist)

    def test__from_args__when_passed_args_for_add_tag_command__the_album_artist_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--album-artist=Various',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Various', command_args.album_artist)

    def test__from_args__when_the_album_artist_has_a_space_in_the_name__the_album_artist_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist="Aphex Twin"',
            '--album-artist="Aphex Twin"',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Aphex Twin', command_args.album_artist)

    def test__from_args__when_the_album_artist_is_not_specified__the_album_artist_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--album=Druqks',
            '--title=Vordhosbn',
            '--year=2001',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=15'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.album_artist)

    def test__from_args__when_passed_args_for_add_tag_command__the_album_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Sturmvogel', command_args.album)

    def test__from_args__when_the_album_has_a_space_in_the_name__the_album_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album="The Teac Life"',
            '--title=Moonmist',
            '--year=2011',
            '--genre=Electronic',
            '--track-number=6',
            '--track-total=14'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('The Teac Life', command_args.album)

    def test__from_args__when_the_album_is_not_specified__the_album_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--title=Moonmist',
            '--year=2011',
            '--genre=Electronic',
            '--track-number=6',
            '--track-total=14'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.album)

    def test__from_args__when_passed_args_for_add_tag_command__the_title_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Pimpshifter', command_args.title)

    def test__from_args__when_the_title_has_a_space_in_the_name__the_title_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Pimpshifter',
            '--title="Geneva Hideout"',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Geneva Hideout', command_args.title)

    def test__from_args__when_the_title_is_not_specified__the_title_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.title)

    def test__from_args__when_passed_args_for_add_tag_command__the_year_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(2000, command_args.year)

    def test__from_args__when_the_year_is_not_specified__the_year_should_be_0(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Pimpshifter',
            '--genre=Electronic',
            '--track-number=2',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(0, command_args.year)

    def test__from_args__when_passed_args_for_add_tag_command__the_track_number_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(1, command_args.track_number)

    def test__from_args__when_the_track_number_is_not_specified__the_track_number_should_be_0(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(0, command_args.track_number)

    def test__from_args__when_passed_args_for_add_tag_command__the_disc_number_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6',
            '--disc-number=1',
            '--disc-total=1',
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(1, command_args.disc_number)

    def test__from_args__when_the_disc_number_is_not_specified__the_disc_number_should_be_0(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(0, command_args.disc_number)

    def test__from_args__when_passed_args_for_add_tag_command__the_genre_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Electronic', command_args.genre)

    def test__from_args__when_the_genre_has_a_space_in_the_name__the_genre_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Pimpshifter',
            '--title="Sturmvogel"',
            '--year=2000',
            '--genre="Cool Jazz"',
            '--track-number=2',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Cool Jazz', command_args.genre)

    def test__from_args__when_the_genre_is_not_specified__the_genre_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Pimpshifter',
            '--title="Sturmvogel"',
            '--year=2000',
            '--track-number=2',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.genre)

    def test__from_args__when_passed_args_for_add_tag_command__the_track_total_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(6, command_args.track_total)

    def test__from_args__when_the_track_total_is_not_specified__the_track_total_should_be_0(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(0, command_args.track_total)

    def test__from_args__when_passed_args_for_add_tag_command__the_disc_total_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6',
            '--disc-number=1',
            '--disc-total=1'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(1, command_args.disc_total)

    def test__from_args__when_the_disc_total_is_not_specified__the_disc_total_should_be_0(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6',
            '--disc-number=1',
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual(0, command_args.disc_total)

    def test__from_args__when_passed_args_for_add_tag_command__the_comment_should_be_specified_correctly(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6',
            '--comment=this_is_a_comment'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('this_is_a_comment', command_args.comment)

    def test__from_args__when_the_comment_is_not_specified__the_comment_should_be_an_empty_string(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('', command_args.comment)

    def test__from_args__when_the_comment_has_a_space_in_the_name__the_comment_should_be_specified_without_surrounding_quotes(self):
        driver = CliDriver()
        arg_parser = driver.get_argument_parser()
        args = arg_parser.parse_args([
            'tag',
            'add',
            'mp3',
            '--source=/some/path/to/song.mp3',
            '--artist=Legowelt',
            '--album=Sturmvogel',
            '--title=Pimpshifter',
            '--year=2000',
            '--genre=Electronic',
            '--track-number=1',
            '--track-total=6',
            '--comment="Warp Records (WARPCD92)"'
        ])
        command_args = AddTagCommandArgs.from_args(args)
        self.assertEqual('Warp Records (WARPCD92)', command_args.comment)
