import unittest
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