import mock
import unittest
from amu.clidriver import DirectorySelector
from tests.helpers import captured_output


class DirectorySelectorTest(unittest.TestCase):
    @mock.patch('amu.clidriver.DirectorySelector._get_input')
    def test__select_directory__list_of_directories_is_provided__the_correct_directories_should_be_printed(self, input_mock):
        input_mock.return_value = '7'
        selector = DirectorySelector()
        with captured_output() as (out, _):
            selector.select_directory([
                'Ambient -- Drone -- Experimental',
                'Early Electronic -- Tape Manipulation',
                'Electronic (By Artist)',
                'Electronic (By Label)',
                'Hip Hop -- Old School Electro',
                'Industrial',
                'Jazz -- Exotica',
                'Library -- Soundtracks',
                'Rock -- Krautrock -- Psychedelic Rock',
            ])
        output = out.getvalue().strip()
        self.assertEqual(
            """Select the directory for the release:
1. Ambient -- Drone -- Experimental
2. Early Electronic -- Tape Manipulation
3. Electronic (By Artist)
4. Electronic (By Label)
5. Hip Hop -- Old School Electro
6. Industrial
7. Jazz -- Exotica
8. Library -- Soundtracks
9. Rock -- Krautrock -- Psychedelic Rock""", output)

    @mock.patch('amu.clidriver.DirectorySelector._get_input')
    def test__select_directory__a_directory_is_selected__the_correct_directory_should_be_returned(self, input_mock):
        input_mock.return_value = '7'
        selector = DirectorySelector()
        selected = selector.select_directory([
            'Ambient -- Drone -- Experimental',
            'Early Electronic -- Tape Manipulation',
            'Electronic (By Artist)',
            'Electronic (By Label)',
            'Hip Hop -- Old School Electro',
            'Industrial',
            'Jazz -- Exotica',
            'Library -- Soundtracks',
            'Rock -- Krautrock -- Psychedelic Rock',
        ])
        self.assertEqual(selected, 'Jazz -- Exotica')
