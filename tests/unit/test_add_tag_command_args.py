""" Test suite for the add tags command args class. """
import unittest
from amu.clidriver import CliDriver
from amu.parsing import AddTagCommandArgs


class AddTagCommandArgsTest(unittest.TestCase):
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
