import unittest
from mock import Mock
from amu.commands import CommandValidationError
from amu.commands import FetchReleaseCommand
from amu.models import ReleaseModel


class FetchReleaseCommandTest(unittest.TestCase):
    def test__validate__a_non_integter_is_used_for_the_id__raises_command_validation_error(self):
        with self.assertRaisesRegexp(CommandValidationError, 'The fetch command must use a valid integer for the discogs ID.'):
            config_service_mock = Mock()
            metadata_service_mock = Mock()
            command = FetchReleaseCommand(config_service_mock, metadata_service_mock)
            command.discogs_id = 'invalid'
            command.validate()

    def test__execute__a_valid_id_is_used__the_metadata_service_returns_a_release_model(self):
        config_service_mock = Mock()
        metadata_service_mock = Mock()
        release_model = ReleaseModel()
        release_model.discogs_id = 12345
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)
        metadata_service_mock.get_release_by_id.return_value = release_model

        command = FetchReleaseCommand(config_service_mock, metadata_service_mock)
        command.discogs_id = 12345
        command.execute()
        metadata_service_mock.get_release_by_id.assert_called_once_with(12345)
