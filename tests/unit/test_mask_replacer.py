import unittest
from amu.metadata import MaskReplacer
from amu.models import ReleaseModel


class MaskReplacerTest(unittest.TestCase):
    def test__replace_directory_mask__label_is_specified_in_mask__label_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%l', release_model)
        self.assertEqual('/music/Bunker Records', replaced_directory)

    def test__replace_directory_mask__artist_is_specified_in_mask__artist_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%a', release_model)
        self.assertEqual('/music/Legowelt', replaced_directory)

    def test__replace_directory_mask__album_is_specified_in_mask__album_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%A', release_model)
        self.assertEqual('/music/Pimpshifter', replaced_directory)

    def test__replace_directory_mask__cat_number_is_specified_in_mask__cat_number_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/[%c]', release_model)
        self.assertEqual('/music/[BUNKER 3002]', replaced_directory)

    def test__replace_directory_mask__country_is_specified_in_mask__country_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%C', release_model)
        self.assertEqual('/music/Netherlands', replaced_directory)

    def test__replace_directory_mask__year_is_specified_in_mask__year_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%y', release_model)
        self.assertEqual('/music/2000', replaced_directory)

    def test__replace_directory_mask__original_year_is_specified_in_mask__original_year_is_replaced_in_mask(self):
        release_model = ReleaseModel()
        release_model.artist = 'Legowelt'
        release_model.title = 'Pimpshifter'
        release_model.label = 'Bunker Records'
        release_model.catno = 'BUNKER 3002'
        release_model.format = 'Vinyl'
        release_model.country = 'Netherlands'
        release_model.year = '2000'
        release_model.original_year = '1998'
        release_model.genre = 'Electronic'
        release_model.style = 'Electro'
        release_model.add_track_directly(None, 'Sturmvogel', 1, 6, 1, 1)
        release_model.add_track_directly(None, 'Geneva Hideout', 2, 6, 1, 1)
        release_model.add_track_directly(None, 'Ricky Ramjet', 3, 6, 1, 1)
        release_model.add_track_directly(None, 'Nuisance Lover', 4, 6, 1, 1)
        release_model.add_track_directly(None, 'Strange Girl', 5, 6, 1, 1)
        release_model.add_track_directly(None, 'Total Pussy Control', 6, 6, 1, 1)

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%Y', release_model)
        self.assertEqual('/music/1998', replaced_directory)

    def test__replace_directory_mask__genre_is_specified_in_mask__genre_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%g', release_model)
        self.assertEqual('/music/Electronic', replaced_directory)

    def test__replace_directory_mask__style_is_specified_in_mask__style_is_replaced_in_mask(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%s', release_model)
        self.assertEqual('/music/Electro', replaced_directory)

    def test__replace_directory_mask__all_masks_are_specified__all_masks_are_replaced(self):
        release_model = ReleaseModel()
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

        mask_replacer = MaskReplacer()
        replaced_directory = mask_replacer.replace_directory_mask('/music/%g/%s/%l/[%c] %a - %A (%C, %y)', release_model)
        self.assertEqual('/music/Electronic/Electro/Bunker Records/[BUNKER 3002] Legowelt - Pimpshifter (Netherlands, 2000)', replaced_directory)

