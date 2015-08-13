import mock
import unittest
from amu.commands import EncodeWavToMp3Command
from amu.models import ReleaseModel
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
