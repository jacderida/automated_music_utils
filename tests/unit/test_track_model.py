import unittest
from amu.models import TrackModel
from tests.helpers import captured_output

class TrackModelTest(unittest.TestCase):
    def test__repr__track_with_single_digit_track_number__should_print_the_padded_track_number(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertRegexpMatches(output, '^01.*')

    def test__repr__track_with_double_digit_track_number__should_print_the_track_number(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 10
        track_model.track_total = 10
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertRegexpMatches(output, '^10.*')

    def test__repr__track_with_double_digit_track_total__should_print_the_track_total(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertRegexpMatches(output, '^01/10.*')

    def test__repr__track_with_single_digit_track_total__should_print_the_padded_track_total(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 6
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertRegexpMatches(output, '^01/06.*')

    def test__repr__track_with_title__should_print_the_title(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 6
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertIn('Xtal', output)

    def test__repr__track_with_single_digit_disc_number__should_print_the_padded_disc_number(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            disc_info = output[-5:]
            self.assertEqual('01/01', disc_info)

    def test__repr__track_with_double_digit_disc_number__should_print_the_disc_number(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 10
        track_model.disc_total = 10

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            disc_info = output[-5:]
            self.assertEqual('10/10', disc_info)

    def test__repr__track_with_single_digit_disc_total__should_print_the_padded_disc_total(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 2
        track_model.disc_total = 2

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            disc_info = output[-5:]
            self.assertEqual('02/02', disc_info)

    def test__repr__track_with_double_digit_disc_total__should_print_the_disc_total(self):
        track_model = TrackModel()
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 20
        track_model.disc_total = 20

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            disc_info = output[-5:]
            self.assertEqual('20/20', disc_info)

    def test__repr__track_with_artist__should_print_the_artist(self):
        track_model = TrackModel()
        track_model.artist = 'Aphex Twin'
        track_model.title = 'Xtal'
        track_model.track_number = 1
        track_model.track_total = 10
        track_model.disc_number = 1
        track_model.disc_total = 1

        with captured_output() as (out, _):
            print track_model
            output = out.getvalue().strip()
            self.assertIn('Aphex Twin', output)
