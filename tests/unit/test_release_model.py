import unittest
from tests.helpers import captured_output
from amu.models import ReleaseModel
from amu.models import TrackModel

class ReleaseModelTest(unittest.TestCase):
    """Test suite for ReleaseModel. """

    def test__add_track__when_adding_a_valid_track__track_is_added_to_collection(self):
        track = TrackModel()
        track.artist = 'Aphex Twin'
        track.title = 'Tha'
        track.position = 2
        release = ReleaseModel()
        release.add_track(track)
        added_track = release.get_tracks()[0]
        self.assertEqual(added_track.artist, 'Aphex Twin')
        self.assertEqual(added_track.title, 'Tha')
        self.assertEqual(added_track.position, 2)

    def test__add_track__when_adding_a_non_track_object__value_error_is_thrown(self):
        with self.assertRaisesRegexp(ValueError, 'The track must be a TrackModel object'):
            release = ReleaseModel()
            release.add_track(1)

    def test__add_track__when_adding_none__value_error_is_thrown(self):
        with self.assertRaisesRegexp(ValueError, 'A non-null value must be supplied for the track'):
            release = ReleaseModel()
            release.add_track(None)

    def test__get_tracks__when_returning_the_tracks__tracks_are_returned_as_tuple(self):
        track = TrackModel()
        track.artist = 'Aphex Twin'
        track.title = 'Tha'
        track.position = 2
        release = ReleaseModel()
        release.add_track(track)
        tracks = release.get_tracks()
        self.assertIsInstance(tracks, tuple)

    def test__repr__populated_release_model__should_print_out_the_discogs_id(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('ID: 12345', output)

    def test__repr__populated_release_model__should_print_out_the_artist(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('Artist: Legowelt', output)

    def test__repr__populated_release_model__should_print_out_the_release_title(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('Title: Pimpshifter', output)

    def test__repr__populated_release_model__should_print_out_the_label(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('Label: Bunker Records', output)

    def test__repr__populated_release_model__should_print_out_the_catno(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('Cat No: BUNKER 3002', output)

    def test__repr__populated_release_model__should_print_out_the_catno(self):
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        with captured_output() as (out, err):
            print release_model
            output = out.getvalue().strip()
            self.assertIn('Format: Vinyl', output)
