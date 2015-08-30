import unittest
from amu.models import TrackModel
from tests.helpers import captured_output

class TrackModelTest(unittest.TestCase):
    def test__repr__track_with_no_artist__should_print_the_track_number(self):
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
