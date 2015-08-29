import mock
import unittest
from amu.commands import EncodeWavToMp3Command
from amu.models import ReleaseModel
from amu.parsing import CommandParsingError
from amu.parsing import MoveAudioFileCommandParser


class TestMoveAudioFileCommandParser(unittest.TestCase):
    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__4_encode_commands__returns_4_move_file_commands(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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

        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_encode_commands(commands, release_model)
        self.assertEqual(4, len(commands))

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__4_encode_commands__source_is_correctly_specified(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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

        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_encode_commands(commands, release_model)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3', commands[0].source)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3', commands[1].source)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3', commands[2].source)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3', commands[3].source)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__4_encode_commands__destination_is_correctly_specified(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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

        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_encode_commands(commands, release_model)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor.Spyboter.A.mp3', commands[3].destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__12_encode_commands__destination_is_correctly_specified(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/01 - Track 01.wav'
        command1.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/02 - Track 02.wav'
        command2.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/03 - Track 03.wav'
        command3.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/04 - Track 04.wav'
        command4.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/04 - Track 04.mp3'
        commands.append(command4)
        command5 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command5.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/05 - Track 05.wav'
        command5.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/05 - Track 05.mp3'
        commands.append(command5)
        command6 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command6.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/06 - Track 06.wav'
        command6.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/06 - Track 06.mp3'
        commands.append(command6)
        command7 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command7.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/07 - Track 07.wav'
        command7.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/07 - Track 07.mp3'
        commands.append(command7)
        command8 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command8.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/08 - Track 08.wav'
        command8.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/08 - Track 08.mp3'
        commands.append(command8)
        command9 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command9.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/09 - Track 09.wav'
        command9.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/09 - Track 09.mp3'
        commands.append(command9)
        command10 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command10.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/10 - Track 10.wav'
        command10.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/10 - Track 10.mp3'
        commands.append(command10)
        command11 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command11.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/11 - Track 11.wav'
        command11.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/11 - Track 11.mp3'
        commands.append(command11)
        command12 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command12.source = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/12 - Track 12.wav'
        command12.destination = '/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/12 - Track 12.mp3'
        commands.append(command12)

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

        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_encode_commands(commands, release_model)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/01 - Acrid Avid Jam Shred.mp3', commands[0].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/02 - The Waxen Pith.mp3', commands[1].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/03 - Wax The Nip.mp3', commands[2].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/04 - Icct Hedral (Edit).mp3', commands[3].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/05 - Ventolin (Video Version).mp3', commands[4].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/06 - Come On You Slags!.mp3', commands[5].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/07 - Start As You Mean To Go On.mp3', commands[6].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/08 - Wet Tip Hen Ax.mp3', commands[7].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/09 - Mookid.mp3', commands[8].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/10 - Alberto Balsalm.mp3', commands[9].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/11 - Cow Cud Is A Twin.mp3', commands[10].destination)
        self.assertEqual('/Warp Records/[WARP CD 30] Aphex Twin - ...I Care Because You Do (1995)/12 - Next Heap With.mp3', commands[11].destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__3_encode_commands_and_release_has_4_tracks__throws_command_parsing_error(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)

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

        with self.assertRaisesRegexp(CommandParsingError, 'The number of encode commands must be the same as the number of tracks on the release.'):
            parser = MoveAudioFileCommandParser(config_mock)
            commands = parser.parse_from_encode_commands(commands, release_model)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_forward_slash_in_title__the_forward_slash_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor/Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_backslash_in_title__the_backslash_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor\Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_question_mark_in_title__the_question_mark_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor?Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_left_arrow_in_title__the_left_arrow_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor<Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_right_arrow_in_title__the_right_arrow_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor>Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_colon_in_title__the_colon_is_replaced_with_a_space(self, config_mock, encoder_mock):
        commands = []
        command1 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command1.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.wav'
        command1.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/01 - Track 01.mp3'
        commands.append(command1)
        command2 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command2.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.wav'
        command2.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/02 - Track 02.mp3'
        commands.append(command2)
        command3 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command3.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.wav'
        command3.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/03 - Track 03.mp3'
        commands.append(command3)
        command4 = EncodeWavToMp3Command(config_mock, encoder_mock)
        command4.source = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.wav'
        command4.destination = '/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Track 04.mp3'
        commands.append(command4)

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
        release_model.add_track_directly(None, 'Backdoor:Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)
