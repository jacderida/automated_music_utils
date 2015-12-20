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

class InvalidMaskError(Exception):
    def __init__(self, message):
        super(InvalidMaskError, self).__init__(message)
        self.message = message

class DiscogsMetadataService(object):
    def get_release_by_id(self, id):
        try:
            client = discogs_client.Client('amu/0.1')
            release = client.release(id)
            release.refresh()
            release_model = ReleaseModel.from_discogs_release(release)
            if release.master != None:
                original_release = client.release(release.master.main_release.id)
                original_release.refresh()
                release_model.original_release = ReleaseModel.from_discogs_release(original_release)
            return release_model
        except HTTPError, ex:
            if ex.status_code == 404:
                raise ReleaseNotFoundError('There is no release with ID {0}.'.format(id))
            raise ex

class MaskReplacer(object):
    def replace_directory_mask(self, masked_directory, release_model):
        mask_options = {
            'l' : release_model.label,
            'a' : release_model.artist,
            'A' : release_model.title,
            'c' : release_model.catno,
            'C' : release_model.country,
            'y' : release_model.year,
            'Y' : release_model.original_release.year if release_model.original_release != None else 'Unknown',
            'g' : release_model.genre,
            's' : release_model.style
        }
        replaced_string = ''
        i = 0
        while i < len(masked_directory):
            char = masked_directory[i]
            if char == '%':
                i += 1
                mask = masked_directory[i]
                replaced_string += self._get_replaced_mask(mask_options, mask)
            else:
                replaced_string += char
            i += 1
        return replaced_string

    def _get_replaced_mask(self, mask_options, mask):
        try:
            return mask_options[mask]
        except KeyError:
            raise InvalidMaskError('The mask {0} is not in the list of valid masks.'.format(mask))
