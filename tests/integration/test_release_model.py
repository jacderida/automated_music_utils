import discogs_client
import unittest
from amu.models import ReleaseModel

class ReleaseModelIntegrationTest(unittest.TestCase):
    def test__from_discogs_release__single_artist_single_label__release_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'Aphex Twin')
        self.assertEqual(release.title, 'Selected Ambient Works 85-92')
        self.assertEqual(release.label, 'Apollo')
        self.assertEqual(release.catno, 'AMB3922RM')
        self.assertEqual(release.format, 'CD, Album, Remastered, Reissue')
        self.assertEqual(release.country, 'Belgium')
        self.assertEqual(release.year, 2008)
        self.assertEqual(release.genre, 'Electronic')
