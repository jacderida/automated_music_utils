import unittest
from amu.clidriver import DirectorySelector
from tests.helpers import captured_output


class DirectorySelectorTest(unittest.TestCase):
    def test__select_directory__list_of_directories_is_provided__the_correct_directories_should_be_printed(self):
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
