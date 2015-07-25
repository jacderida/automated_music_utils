import discogs_client
import sys
from discogs_client.exceptions import HTTPError
from amu.models import ReleaseModel


class ReleaseNotFoundError(Exception):
    def __init__(self, message):
        super(ReleaseNotFoundError, self).__init__(message)
        self.message = message

class DiscogsMetadataService(object):
    def get_release_by_id(self, id):
        try:
            client = discogs_client.Client('amu/0.1')
            release = client.release(id)
            release.refresh()
            return ReleaseModel.from_discogs_release(release)
        except HTTPError, ex:
            if ex.status_code == 404:
                raise ReleaseNotFoundError('There is no release with ID {0}.'.format(id))
            raise ex
