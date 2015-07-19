import discogs_client
import unittest
from amu.models import TrackModel

class TrackModelIntegrationTest(unittest.TestCase):
    def test__from_discogs_track__track_with_no_artist__track_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[0], 1, 13, 1, 1)
        self.assertEqual(track.track_number, 1)
        self.assertEqual(track.track_total, 13)
        self.assertEqual(track.disc_number, 1)
        self.assertEqual(track.disc_total, 1)
        self.assertEqual(track.title, 'Xtal')
        self.assertEqual(track.artist, '')

    def test__from_discogs_track__track_has_an_artist__track_has_artist(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1144083)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[2], 3, 3, 1, 1)
        self.assertEqual(track.track_number, 3)
        self.assertEqual(track.track_total, 3)
        self.assertEqual(track.disc_number, 1)
        self.assertEqual(track.disc_total, 1)
        self.assertEqual(track.title, 'Conquestadores Extraterrestriales (Remix)')
        self.assertEqual(track.artist, 'Legowelt')

    def test__from_discogs_track__track_has_artist_with_anv__anv_is_resolved(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(494794)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[2], 3, 4, 1, 1)
        self.assertEqual(track.track_number, 3)
        self.assertEqual(track.track_total, 4)
        self.assertEqual(track.disc_number, 1)
        self.assertEqual(track.disc_total, 1)
        self.assertEqual(track.title, '46 Analord-Masplid')
        self.assertEqual(track.artist, 'AFX')

    def test__from_discogs_track__track_has_multiple_artists__the_joined_artist_is_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(3646941)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[20], 21, 48, 1, 1)
        self.assertEqual(track.artist, 'Brian Bennett / Warren Bennett')

    def test__from_discogs_track__track_has_artists_with_multiple_anvs__the_anvs_are_resolved(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1606562)
        track = TrackModel.from_discogs_track(discogs_release.tracklist[2], 3, 15, 1, 1)
        self.assertEqual(track.artist, 'L. Hurdle / F. Ricotti')
