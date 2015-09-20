import mock
import unittest
from amu.commands import EncodeWavToMp3Command
from amu.models import ReleaseModel
from amu.parsing import CommandParsingError
from amu.parsing import MoveAudioFileCommandParser
from mock import Mock


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

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_asterisk_in_title__the_asterisk_is_replaced_with_a_space(self, config_mock, encoder_mock):
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
        release_model.add_track_directly(None, 'Backdoor*Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_pipe_in_title__the_pipe_is_replaced_with_a_space(self, config_mock, encoder_mock):
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
        release_model.add_track_directly(None, 'Backdoor|Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('amu.encode.LameEncoder')
    @mock.patch('amu.config.ConfigurationProvider')
    def test__parse_from_encode_commands__track_has_double_quote_in_title__the_double_quote_is_replaced_with_a_space(self, config_mock, encoder_mock):
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
        release_model.add_track_directly(None, 'Backdoor"Spyboter.A', 4, 4, 1, 1)

        parser = MoveAudioFileCommandParser(config_mock)
        command = parser.parse_from_encode_commands(commands, release_model)[3]
        self.assertEqual('/Rephlex/[ANALORD 08] AFX - Analord 08 (2005)/04 - Backdoor Spyboter.A.mp3', command.destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_4_tracks__4_move_file_commands_are_generated(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True

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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual(4, len(commands))

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_4_tracks__source_is_set_correctly(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/source/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/04 - Track 4.mp3', commands[3].source)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_4_tracks_and_walk_returns_tracks_in_arbitrary_order__source_is_set_correctly(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('02 - Track 2.mp3', '01 - Track 1.mp3', '04 - Track 4.mp3', '03 - Track 3.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/source/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/04 - Track 4.mp3', commands[3].source)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_4_tracks__destination_is_set_correctly(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor.Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_forward_slash__forward_slash_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_back_slash__back_slash_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_question_mark__question_mark_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_left_arrow__left_arrow_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_right_arrow__right_arrow_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_colon__colon_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_asterisk__asterisk_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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
        release_model.add_track_directly(None, 'Backdoor*Spyboter.A', 4, 4, 1, 1)

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_pipe__pipe_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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
        release_model.add_track_directly(None, 'Backdoor|Spyboter.A', 4, 4, 1, 1)

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_has_track_title_with_double_quotes__double_quotes_is_replaced_with_a_space(self, walk_mock, isdir_mock):
        walk_mock.return_value = [
            ('/some/source', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3'))
        ]
        isdir_mock.return_value = True
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
        release_model.add_track_directly(None, 'Backdoor"Spyboter.A', 4, 4, 1, 1)

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model('/some/source', '/some/destination', release_model)
        self.assertEqual('/some/destination/01 - PWSteal.Ldpinch.D.mp3', commands[0].destination)
        self.assertEqual('/some/destination/02 - Backdoor.Berbew.Q.mp3', commands[1].destination)
        self.assertEqual('/some/destination/03 - W32.Deadcode.A.mp3', commands[2].destination)
        self.assertEqual('/some/destination/04 - Backdoor Spyboter.A.mp3', commands[3].destination)

    @mock.patch('os.path.isdir')
    def test__parse_from_release_model__source_is_not_a_directory__command_parsing_error_is_raised(self, isdir_mock):
        isdir_mock.return_value = False
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
        release_model.add_track_directly(None, 'Backdoor"Spyboter.A', 4, 4, 1, 1)

        with self.assertRaisesRegexp(CommandParsingError, 'The source must be a directory.'):
            config_mock = Mock()
            parser = MoveAudioFileCommandParser(config_mock)
            parser.parse_from_release_model('/some/source/file.mp3', '/some/destination', release_model)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_is_multi_cd__destination_is_set_correctly(self, walk_mock, listdir_mock, isdir_mock):
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
        release_model.add_track_directly('Nobukazu Takemura', 'Let My Fish Loose (Aphex Twin Remix)', 13, 13, 1, 2)
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
        source_path = '/some/source'
        walk_mock.return_value = [
            (source_path, ('cd1', 'cd2'), ()),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3']
        ]
        isdir_mock.return_value = True

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, '/some/destination', release_model)
        self.assertEqual('/some/destination/cd1/01 - Time To Find Me (AFX Fast Mix).mp3', commands[0].destination)
        self.assertEqual('/some/destination/cd1/02 - Raising The Titanic (Big Drum Mix).mp3', commands[1].destination)
        self.assertEqual('/some/destination/cd1/03 - Journey (Aphex Twin Care Mix).mp3', commands[2].destination)
        self.assertEqual('/some/destination/cd1/04 - Triachus (Mix By Aphex Twin).mp3', commands[3].destination)
        self.assertEqual('/some/destination/cd1/05 - Hereos (Aphex Twin Remix).mp3', commands[4].destination)
        self.assertEqual('/some/destination/cd1/06 - In The Glitter Part 2 (Aphex Twin Mix).mp3', commands[5].destination)
        self.assertEqual('/some/destination/cd1/07 - Zeros And Ones (Aphex Twin Reconstruction #2).mp3', commands[6].destination)
        self.assertEqual('/some/destination/cd1/08 - Ziggy (Aphex Twin Mix #1).mp3', commands[7].destination)
        self.assertEqual('/some/destination/cd1/09 - Your Head My Voice (Voix Revirement).mp3', commands[8].destination)
        self.assertEqual('/some/destination/cd1/10 - Change (Aphex Twin Mix #1).mp3', commands[9].destination)
        self.assertEqual("/some/destination/cd1/11 - Une Femme N'est Pas Un Homme (Aphex Twin Mix).mp3", commands[10].destination)
        self.assertEqual('/some/destination/cd1/12 - The Beauty Of Being Numb Section B (Created By Aphex Twin).mp3', commands[11].destination)
        self.assertEqual('/some/destination/cd1/13 - Let My Fish Loose (Aphex Twin Remix).mp3', commands[12].destination)
        self.assertEqual('/some/destination/cd2/01 - Kreiger (Aphex Twin Baldhu Mix).mp3', commands[13].destination)
        self.assertEqual('/some/destination/cd2/02 - Deep In Velvet (Aphex Twin Turnips Mix).mp3', commands[14].destination)
        self.assertEqual('/some/destination/cd2/03 - Falling Free (Aphex Twin Remix).mp3', commands[15].destination)
        self.assertEqual('/some/destination/cd2/04 - We Have Arrived (Aphex Twin QQT Mix).mp3', commands[16].destination)
        self.assertEqual('/some/destination/cd2/05 - At The Heart Of It All (Created By Aphex Twin).mp3', commands[17].destination)
        self.assertEqual('/some/destination/cd2/06 - Flow Coma (Remix By AFX).mp3', commands[18].destination)
        self.assertEqual('/some/destination/cd2/07 - Window Licker (Acid Edit).mp3', commands[19].destination)
        self.assertEqual('/some/destination/cd2/08 - Normal (Helston Flora Remix By AFX).mp3', commands[20].destination)
        self.assertEqual('/some/destination/cd2/09 - SAW2 CD1 TRK2 (Original Mix).mp3', commands[21].destination)
        self.assertEqual('/some/destination/cd2/10 - Mindstream (The Aphex Twin Remix).mp3', commands[22].destination)
        self.assertEqual("/some/destination/cd2/11 - You Can't Hide Your Love (Hidden Love Mix).mp3", commands[23].destination)
        self.assertEqual('/some/destination/cd2/12 - Spotlight (Aphex Twin Mix).mp3', commands[24].destination)
        self.assertEqual('/some/destination/cd2/13 - Debase (Soft Palate).mp3', commands[25].destination)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_is_multi_cd_and_walk_returns_directories_in_arbitrary_order__source_is_set_correctly(self, walk_mock, listdir_mock, isdir_mock):
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
        release_model.add_track_directly('Nobukazu Takemura', 'Let My Fish Loose (Aphex Twin Remix)', 13, 13, 1, 2)
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
        source_path = '/some/source'
        walk_mock.return_value = [
            (source_path, ('cd2', 'cd1'), ()),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
        ]
        listdir_mock.side_effect = [
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3'],
            ['01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3']
        ]
        isdir_mock.return_value = True

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, '/some/destination', release_model)
        self.assertEqual('/some/source/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/cd1/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/cd1/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/cd1/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/source/cd1/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/source/cd1/06 - Track 6.mp3', commands[5].source)
        self.assertEqual('/some/source/cd1/07 - Track 7.mp3', commands[6].source)
        self.assertEqual('/some/source/cd1/08 - Track 8.mp3', commands[7].source)
        self.assertEqual('/some/source/cd1/09 - Track 9.mp3', commands[8].source)
        self.assertEqual('/some/source/cd1/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/source/cd1/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/source/cd1/12 - Track 12.mp3', commands[11].source)
        self.assertEqual('/some/source/cd1/13 - Track 13.mp3', commands[12].source)
        self.assertEqual('/some/source/cd2/01 - Track 1.mp3', commands[13].source)
        self.assertEqual('/some/source/cd2/02 - Track 2.mp3', commands[14].source)
        self.assertEqual('/some/source/cd2/03 - Track 3.mp3', commands[15].source)
        self.assertEqual('/some/source/cd2/04 - Track 4.mp3', commands[16].source)
        self.assertEqual('/some/source/cd2/05 - Track 5.mp3', commands[17].source)
        self.assertEqual('/some/source/cd2/06 - Track 6.mp3', commands[18].source)
        self.assertEqual('/some/source/cd2/07 - Track 7.mp3', commands[19].source)
        self.assertEqual('/some/source/cd2/08 - Track 8.mp3', commands[20].source)
        self.assertEqual('/some/source/cd2/09 - Track 9.mp3', commands[21].source)
        self.assertEqual('/some/source/cd2/10 - Track 10.mp3', commands[22].source)
        self.assertEqual("/some/source/cd2/11 - Track 11.mp3", commands[23].source)
        self.assertEqual('/some/source/cd2/12 - Track 12.mp3', commands[24].source)
        self.assertEqual('/some/source/cd2/13 - Track 13.mp3', commands[25].source)

    @mock.patch('os.path.isdir')
    @mock.patch('os.listdir')
    @mock.patch('os.walk')
    def test__parse_from_release_model__release_is_multi_cd_and_listdir_returns_files_in_arbitrary_order__source_is_set_correctly(self, walk_mock, listdir_mock, isdir_mock):
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
        release_model.add_track_directly('Nobukazu Takemura', 'Let My Fish Loose (Aphex Twin Remix)', 13, 13, 1, 2)
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
        source_path = '/some/source'
        walk_mock.return_value = [
            (source_path, ('cd2', 'cd1'), ()),
            (source_path + '/cd2', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
            (source_path + '/cd1', (), ('01 - Track 1.mp3', '02 - Track 2.mp3', '03 - Track 3.mp3', '04 - Track 4.mp3', '05 - Track 5.mp3', '06 - Track 6.mp3', '07 - Track 7.mp3', '08 - Track 8.mp3', '09 - Track 9.mp3', '10 - Track 10.mp3', '11 - Track 11.mp3', '12 - Track 12.mp3', '13 - Track 13.mp3')),
        ]
        listdir_mock.side_effect = [
            ['02 - Track 2.mp3', '01 - Track 1.mp3', '03 - Track 3.mp3', '05 - Track 5.mp3', '04 - Track 4.mp3', '07 - Track 7.mp3', '06 - Track 6.mp3', '08 - Track 8.mp3', '10 - Track 10.mp3', '09 - Track 9.mp3', '11 - Track 11.mp3', '13 - Track 13.mp3', '12 - Track 12.mp3'],
            ['02 - Track 2.mp3', '01 - Track 1.mp3', '03 - Track 3.mp3', '05 - Track 5.mp3', '04 - Track 4.mp3', '07 - Track 7.mp3', '06 - Track 6.mp3', '08 - Track 8.mp3', '10 - Track 10.mp3', '09 - Track 9.mp3', '11 - Track 11.mp3', '13 - Track 13.mp3', '12 - Track 12.mp3'],
        ]
        isdir_mock.return_value = True

        config_mock = Mock()
        parser = MoveAudioFileCommandParser(config_mock)
        commands = parser.parse_from_release_model(source_path, '/some/destination', release_model)
        self.assertEqual('/some/source/cd1/01 - Track 1.mp3', commands[0].source)
        self.assertEqual('/some/source/cd1/02 - Track 2.mp3', commands[1].source)
        self.assertEqual('/some/source/cd1/03 - Track 3.mp3', commands[2].source)
        self.assertEqual('/some/source/cd1/04 - Track 4.mp3', commands[3].source)
        self.assertEqual('/some/source/cd1/05 - Track 5.mp3', commands[4].source)
        self.assertEqual('/some/source/cd1/06 - Track 6.mp3', commands[5].source)
        self.assertEqual('/some/source/cd1/07 - Track 7.mp3', commands[6].source)
        self.assertEqual('/some/source/cd1/08 - Track 8.mp3', commands[7].source)
        self.assertEqual('/some/source/cd1/09 - Track 9.mp3', commands[8].source)
        self.assertEqual('/some/source/cd1/10 - Track 10.mp3', commands[9].source)
        self.assertEqual('/some/source/cd1/11 - Track 11.mp3', commands[10].source)
        self.assertEqual('/some/source/cd1/12 - Track 12.mp3', commands[11].source)
        self.assertEqual('/some/source/cd1/13 - Track 13.mp3', commands[12].source)
        self.assertEqual('/some/source/cd2/01 - Track 1.mp3', commands[13].source)
        self.assertEqual('/some/source/cd2/02 - Track 2.mp3', commands[14].source)
        self.assertEqual('/some/source/cd2/03 - Track 3.mp3', commands[15].source)
        self.assertEqual('/some/source/cd2/04 - Track 4.mp3', commands[16].source)
        self.assertEqual('/some/source/cd2/05 - Track 5.mp3', commands[17].source)
        self.assertEqual('/some/source/cd2/06 - Track 6.mp3', commands[18].source)
        self.assertEqual('/some/source/cd2/07 - Track 7.mp3', commands[19].source)
        self.assertEqual('/some/source/cd2/08 - Track 8.mp3', commands[20].source)
        self.assertEqual('/some/source/cd2/09 - Track 9.mp3', commands[21].source)
        self.assertEqual('/some/source/cd2/10 - Track 10.mp3', commands[22].source)
        self.assertEqual("/some/source/cd2/11 - Track 11.mp3", commands[23].source)
        self.assertEqual('/some/source/cd2/12 - Track 12.mp3', commands[24].source)
        self.assertEqual('/some/source/cd2/13 - Track 13.mp3', commands[25].source)
