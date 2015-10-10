import mock
import unittest
from amu.commands import AddTagCommand
from amu.commands import MoveAudioFileCommand
from amu.parsing import AddTagCommandArgs
from amu.parsing import CommandParsingError
from amu.parsing import MixCommandParser
from mock import Mock

class MixCommandParserTest(unittest.TestCase):
    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_generate_an_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertIsInstance(commands[0], AddTagCommand)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_artist_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].artist, 'Aphex Twin')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_artist_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album_artist, 'Aphex Twin')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_album_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].album, "All Tomorrow's Parties")

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_title_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].title, "All Tomorrow's Parties")

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_year_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].year, '2003')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_comment_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].comment, "DJ Set at All Tomorrow's Parties 2003")

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_genre_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].genre, 'Mixes')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_track_number_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].track_number, 1)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_track_total_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].track_total, 1)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_disc_number_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].disc_number, 1)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_disc_total_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].disc_total, 1)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_source_on_the_add_tag_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[0].source, '/some/source/track.mp3')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_generate_a_move_file_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertIsInstance(commands[1], MoveAudioFileCommand)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_source_on_the_move_file_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[1].source, '/some/source/track.mp3')

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__source_is_empty__raises_value_error(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = ''
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        with self.assertRaisesRegexp(ValueError, 'A value must be supplied for the source.'):
            mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
            mix_command_parser.parse_mix_command(tag_command_args)

    @mock.patch('os.path.isfile')
    def test__parse_mix_command__single_file_mix__it_should_specify_the_destination_on_the_move_file_command(self, isfile_mock):
        isfile_mock.return_value = True
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source/track.mp3'
        tag_command_args.artist = 'Aphex Twin'
        tag_command_args.album = "All Tomorrow's Parties"
        tag_command_args.title = "All Tomorrow's Parties"
        tag_command_args.year = '2003'
        tag_command_args.comment = "DJ Set at All Tomorrow's Parties 2003"
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = mix_command_parser.parse_mix_command(tag_command_args)
        self.assertEqual(commands[1].destination, '/mixes/destination/track.mp3')

    @mock.patch('os.path.isfile')
    @mock.patch('os.listdir')
    def test__parse_mix_command__source_is_directory_with_4_files__it_should_generate_4_add_tag_commands(self, listdir_mock, isfile_mock):
        isfile_mock.return_value = False
        listdir_mock.return_value = [
            'Autechre-2006-12-28-part01_vbr.mp3',
            'Autechre-2006-12-28-part02_vbr.mp3',
            'Autechre-2006-12-28-part03_vbr.mp3',
            'Autechre-2006-12-28-part04_vbr.mp3'
        ]
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source'
        tag_command_args.artist = 'Autechre'
        tag_command_args.album = 'Xltronic Marathon'
        tag_command_args.title = 'Xltronic Marathon'
        tag_command_args.year = '2006'
        tag_command_args.comment = 'Broadcast on Xltronic on 28/12/2006.'
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = [x for x in mix_command_parser.parse_mix_command(tag_command_args) if isinstance(x, AddTagCommand)]
        self.assertEqual(len(commands), 4)

    @mock.patch('os.path.isfile')
    @mock.patch('os.listdir')
    def test__parse_mix_command__source_is_directory_with_4_files__it_should_generate_4_move_file_commands(self, listdir_mock, isfile_mock):
        isfile_mock.return_value = False
        listdir_mock.return_value = [
            'Autechre-2006-12-28-part01_vbr.mp3',
            'Autechre-2006-12-28-part02_vbr.mp3',
            'Autechre-2006-12-28-part03_vbr.mp3',
            'Autechre-2006-12-28-part04_vbr.mp3'
        ]
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source'
        tag_command_args.artist = 'Autechre'
        tag_command_args.album = 'Xltronic Marathon'
        tag_command_args.title = 'Xltronic Marathon'
        tag_command_args.year = '2006'
        tag_command_args.comment = 'Broadcast on Xltronic on 28/12/2006.'
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = [x for x in mix_command_parser.parse_mix_command(tag_command_args) if isinstance(x, MoveAudioFileCommand)]
        self.assertEqual(len(commands), 4)

    @mock.patch('os.path.isfile')
    @mock.patch('os.listdir')
    def test__parse_mix_command__source_is_directory_with_4_files__it_should_specify_the_source_correctly_on_the_add_tag_commands(self, listdir_mock, isfile_mock):
        isfile_mock.return_value = False
        listdir_mock.return_value = [
            'Autechre-2006-12-28-part01_vbr.mp3',
            'Autechre-2006-12-28-part02_vbr.mp3',
            'Autechre-2006-12-28-part03_vbr.mp3',
            'Autechre-2006-12-28-part04_vbr.mp3'
        ]
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source'
        tag_command_args.artist = 'Autechre'
        tag_command_args.album = 'Xltronic Marathon'
        tag_command_args.title = 'Xltronic Marathon'
        tag_command_args.year = '2006'
        tag_command_args.comment = 'Broadcast on Xltronic on 28/12/2006.'
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = [x for x in mix_command_parser.parse_mix_command(tag_command_args) if isinstance(x, AddTagCommand)]
        self.assertEqual(commands[0].source, '/some/source/Autechre-2006-12-28-part01_vbr.mp3')
        self.assertEqual(commands[1].source, '/some/source/Autechre-2006-12-28-part02_vbr.mp3')
        self.assertEqual(commands[2].source, '/some/source/Autechre-2006-12-28-part03_vbr.mp3')
        self.assertEqual(commands[3].source, '/some/source/Autechre-2006-12-28-part04_vbr.mp3')

    @mock.patch('os.path.isfile')
    @mock.patch('os.listdir')
    def test__parse_mix_command__source_is_directory_with_4_files__it_should_specify_the_source_correctly_on_the_move_file_commands(self, listdir_mock, isfile_mock):
        isfile_mock.return_value = False
        listdir_mock.return_value = [
            'Autechre-2006-12-28-part01_vbr.mp3',
            'Autechre-2006-12-28-part02_vbr.mp3',
            'Autechre-2006-12-28-part03_vbr.mp3',
            'Autechre-2006-12-28-part04_vbr.mp3'
        ]
        tag_command_args = AddTagCommandArgs()
        tag_command_args.source = '/some/source'
        tag_command_args.artist = 'Autechre'
        tag_command_args.album = 'Xltronic Marathon'
        tag_command_args.title = 'Xltronic Marathon'
        tag_command_args.year = '2006'
        tag_command_args.comment = 'Broadcast on Xltronic on 28/12/2006.'
        config_provider_mock, tagger_mock = (Mock(),)*2
        config_provider_mock.get_mixes_destination.return_value = '/mixes/destination'
        mix_command_parser = MixCommandParser(config_provider_mock, tagger_mock)
        commands = [x for x in mix_command_parser.parse_mix_command(tag_command_args) if isinstance(x, MoveAudioFileCommand)]
        self.assertEqual(commands[0].source, '/some/source/Autechre-2006-12-28-part01_vbr.mp3')
        self.assertEqual(commands[1].source, '/some/source/Autechre-2006-12-28-part02_vbr.mp3')
        self.assertEqual(commands[2].source, '/some/source/Autechre-2006-12-28-part03_vbr.mp3')
        self.assertEqual(commands[3].source, '/some/source/Autechre-2006-12-28-part04_vbr.mp3')
