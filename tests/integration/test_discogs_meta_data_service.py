import unittest
from amu.metadata import DiscogsMetadataService
from amu.metadata import ReleaseNotFoundError
from amu.models import ReleaseModel

class DiscogsMetadataServiceTest(unittest.TestCase):
    def test__get_release_by_id__valid_release_id__returns_populated_release_model(self):
        service = DiscogsMetadataService()
        release = service.get_release_by_id(32662)
        self.assertEqual(32662, release.discogs_id)

    def test__get_release_by_id__invalid_release_id__raises_release_not_found_error(self):
        with self.assertRaisesRegexp(ReleaseNotFoundError, 'There is no release with ID invalid_id.'):
            service = DiscogsMetadataService()
            service.get_release_by_id('invalid_id')

    def test__from_discogs_release__release_is_reissue__the_original_label_details_should_be_populated(self):
        service = DiscogsMetadataService()
        release = service.get_release_by_id(792244)
        self.assertIsNotNone(release.original_release)
        self.assertEqual(release.original_release.year, '1969')
        self.assertEqual(release.original_release.label, 'Liberty')
        self.assertEqual(release.original_release.catno, 'LBS 83 279 I')

    def test__from_discogs_release__collapse_index_tracks_is_specified__the_original_label_details_should_be_populated(self):
        service = DiscogsMetadataService()
        release = service.get_release_by_id(3579489, collapse_index_tracks=True)
        self.assertEqual(7, len(release.get_tracks()))
