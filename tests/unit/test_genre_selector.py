import mock
import unittest
from amu.clidriver import GenreSelector
from tests.helpers import captured_output


class GenreSelectorTests(unittest.TestCase):
    @mock.patch('amu.clidriver.DirectorySelector._get_input')
    def test__select_genre__list_of_genres_is_provided__the_correct_genres_should_be_printed(self, input_mock):
        input_mock.return_value = '7'
        selector = GenreSelector()
        with captured_output() as (out, _):
            selector.select_genre([
                'Electronic',
                'Techno',
                'Electro',
                'Experimental',
                'Ambient',
            ])
        output = out.getvalue().strip()
        self.assertEqual(
            """Select the genre from what's available from the discogs release, or provide a free text value:
1. Electronic
2. Techno
3. Electro
4. Experimental
5. Ambient""", output)
