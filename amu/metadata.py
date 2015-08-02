"""
A module for classes that are concerned with music metadata.
"""
import discogs_client
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

class MaskReplacer(object):
    def replace_directory_mask(self, masked_directory, release_model):
        replaced_string = ''
        i = 0
        while i < len(masked_directory):
            char = masked_directory[i]
            if char == '%':
                i += 1
                mask = masked_directory[i]
                if mask == 'l':
                    replaced_string += release_model.label
                elif mask == 'a':
                    replaced_string += release_model.artist
            else:
                replaced_string += char
            i += 1
        return replaced_string
