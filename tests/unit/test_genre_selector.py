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
    def test__select_genre__a_numeric_selection_is_made_from_provided_list__the_correct_genre_should_be_returned(self, input_mock):
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

    @mock.patch('amu.clidriver.GenreSelector._get_input')
    def test__select_genre__a_numeric_selection_is_made_that_is_less_than_1__it_should_prompt_to_re_enter_input(self, input_mock):
        input_mock.side_effect = ['0', '3']
        with captured_output() as (out, _):
            selector = GenreSelector()
            selected = selector.select_genre([
                'Electronic',
                'Techno',
                'Electro',
                'Experimental',
                'Ambient',
            ])
        output = out.getvalue().strip()
        self.assertIn('Please enter a value between 1 and 5.', output)

    @mock.patch('amu.clidriver.GenreSelector._get_input')
    def test__select_genre__a_numeric_selection_is_made_that_is_greater_than_genre_length__it_should_prompt_to_re_enter_input(self, input_mock):
        input_mock.side_effect = ['6', '3']
        with captured_output() as (out, _):
            selector = GenreSelector()
            selected = selector.select_genre([
                'Electronic',
                'Techno',
                'Electro',
                'Experimental',
                'Ambient',
            ])
        output = out.getvalue().strip()
        self.assertIn('Please enter a value between 1 and 5.', output)

    @mock.patch('amu.clidriver.GenreSelector._get_input')
    def test__select_genre__a_free_text_selection_is_made__it_should_return_the_free_text_selection(self, input_mock):
        input_mock.side_effect = ['Early Electronic']
        selector = GenreSelector()
        selected = selector.select_genre([
            'Electronic',
            'Techno',
            'Electro',
            'Experimental',
            'Ambient',
        ])
        self.assertEqual('Early Electronic', selected)
