import discogs_client
import unittest
from amu.models import TrackModel

class TrackModelIntegrationTest(unittest.TestCase):
    def test__from_discogs_track__track_with_no_artist__track_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[0], 1)
        self.assertEqual(track.position, 1)
        self.assertEqual(track.title, 'Xtal')
        self.assertEqual(track.artist, '')

    def test__from_discogs_track__track_has_an_artist__track_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1144083)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[2], 3)
        self.assertEqual(track.position, 3)
        self.assertEqual(track.title, 'Conquestadores Extraterrestriales (Remix)')
        self.assertEqual(track.artist, 'Legowelt')
