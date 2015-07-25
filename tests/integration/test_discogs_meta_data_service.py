import unittest
from amu.metadata import DiscogsMetadataService
from amu.metadata import ReleaseNotFoundError
from amu.models import ReleaseModel

class DiscogsMetadataServiceTest(unittest.TestCase):
    def test__get_release_by_id__valid_release_id__returns_populated_release_model(self):
        service = DiscogsMetadataService()
        release = service.get_release_by_id(32662)
        self.assertEqual(32662, release.id)

    def test__get_release_by_id__invalid_release_id__raises_release_not_found_error(self):
        with self.assertRaisesRegexp(ReleaseNotFoundError, 'There is no release with ID invalid_id.'):
            service = DiscogsMetadataService()
            service.get_release_by_id('invalid_id')
