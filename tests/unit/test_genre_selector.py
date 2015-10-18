import mock
import unittest
from amu.clidriver import GenreSelector
from tests.helpers import captured_output


class GenreSelectorTests(unittest.TestCase):
    @mock.patch('amu.clidriver.GenreSelector._get_input')
    def test__select_genre__list_of_genres_is_provided__the_correct_genres_should_be_printed(self, input_mock):
        input_mock.return_value = '3'
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

    @mock.patch('amu.clidriver.GenreSelector._get_input')
    def test__select_genre__a_genre_is_selected__the_correct_genre_should_be_returned(self, input_mock):
        input_mock.return_value = '3'
        selector = GenreSelector()
        selected = selector.select_genre([
            'Electronic',
            'Techno',
            'Electro',
            'Experimental',
            'Ambient',
        ])
        self.assertEqual(selected, 'Electro')
