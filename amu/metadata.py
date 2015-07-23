import discogs_client
from amu.models import ReleaseModel


class DiscogsMetadataService(object):
    def get_release_by_id(self, id):
        client = discogs_client.Client('amu/0.1')
        release = client.release(id)
        release.refresh()
        return ReleaseModel.from_discogs_release(release)
