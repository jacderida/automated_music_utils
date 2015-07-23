import unittest
from amu.metadata import DiscogsMetadataService
from amu.models import ReleaseModel

class DiscogsMetadataServiceTest(unittest.TestCase):
    def test__get_release_by_id__valid_release_id__returns_populated_release_model(self):
        service = DiscogsMetadataService()
        release = service.get_release_by_id(32662)
        self.assertEqual(32662, release.id)
