import os
import shutil
import unittest

import mock

from amu.audio import FlacTagger, TaggerError
from tests.helpers import get_flac_artwork_data
from tests.helpers import get_flac_tag_data
from tests.helpers import flac_has_tags


class FlacTaggerTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.flac', 'tests/integration/data/test_data.flac')
        shutil.copyfile('tests/integration/data/song_with_tags.flac', 'tests/integration/data/test_data_song_with_tags.flac')

    def tearDown(self):
        os.remove('tests/integration/data/test_data.flac')

    def test__add_tags__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be set for tagging a flac.'):
            tagger = FlacTagger()
            tagger.add_tags('')

    @mock.patch('os.path.exists')
    def test__add_tags__source_does_not_exist__raises_tagger_error(self, exists_mock):
        exists_mock.return_value = False
        with self.assertRaisesRegexp(TaggerError, 'The source /some/non/existent/flac does not exist.'):
            tagger = FlacTagger()
            tagger.add_tags('/some/non/existent/flac')

    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    def test__add_tags__source_is_directory__raises_tagger_error(self, exists_mock, isdir_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = True
        with self.assertRaisesRegexp(TaggerError, 'The source must not be a directory.'):
            tagger = FlacTagger()
            tagger.add_tags('/some/non/existent/flac')

    def test__add_tags__artist_is_set__tag_should_have_an_artist_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', artist='Aphex Twin')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['artist'], u'Aphex Twin')

    def test__add_tags__artist_is_not_set__tag_should_not_have_an_artist_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('artist'))

    def test__add_tags__album_artist_is_set__tag_should_have_an_album_artist_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', album_artist='Various')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['album_artist'], u'Various')

    def test__add_tags__album_artist_is_not_set__tag_should_not_have_an_album_artist_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('album_artist'))

    def test__add_tags__title_is_set__tag_should_have_a_title_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', title='Flap Head')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['title'], u'Flap Head')

    def test__add_tags__title_is_not_set__tag_should_not_have_a_title_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('title'))

    def test__add_tags__album_is_set__tag_should_have_an_album_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', album='Dark Side of the Moon')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['album'], u'Dark Side of the Moon')

    def test__add_tags__album_is_not_set__tag_should_not_have_an_album_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('album'))

    def test__add_tags__year_is_set__tag_should_have_a_year_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', year='2015')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['year'], u'2015')

    def test__add_tags__year_is_not_set__tag_should_not_have_a_year_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('year'))

    def test__add_tags__genre_is_set__tag_should_have_a_genre_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', genre='Electronic')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['genre'], u'Electronic')

    def test__add_tags__genre_is_not_set__tag_should_not_have_a_genre_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('genre'))

    def test__add_tags__comment_is_set__tag_should_have_a_comment_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', comment='WARPCD92')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['comment'], u'WARPCD92')

    def test__add_tags__comment_is_not_set__tag_should_not_have_a_comment_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac')
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertFalse(tag_data.has_key('comment'))

    def test__add_tags__track_number_is_set__tag_should_have_a_track_number_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', track_number=10, track_total=15)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['trackno'], u'10/15')

    def test__add_tags__track_number_is_less_than_10__tag_should_have_a_padded_track_number_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', track_number=5, track_total=15)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['trackno'], u'05/15')

    def test__add_tags__track_total_is_less_than_10__tag_should_have_a_padded_track_total_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', track_number=5, track_total=6)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['trackno'], u'05/06')

    def test__add_tags__disc_number_is_set__tag_should_have_a_disc_number_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', disc_number=13, disc_total=14)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['discno'], u'13/14')

    def test__add_tags__disc_number_is_less_than_10__tag_should_have_a_padded_disc_number_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', disc_number=3, disc_total=14)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['discno'], u'03/14')

    def test__add_tags__disc_total_is_less_than_10__tag_should_have_a_padded_disc_total_frame(self):
        tagger = FlacTagger()
        tagger.add_tags('tests/integration/data/test_data.flac', disc_number=3, disc_total=4)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['discno'], u'03/04')

    def test__add_tags__all_fields_specified__tag_should_have_all_frames_set(self):
        tagger = FlacTagger()
        tagger.add_tags(
            'tests/integration/data/test_data.flac', 'Aphex Twin', 'Aphex Twin', 'Drukqs',
            'Flap Head', '2015', 'Electronic', 'Nightwind Records (NW001)', 5, 6, 1, 1)
        tag_data = get_flac_tag_data('tests/integration/data/test_data.flac')
        self.assertEqual(tag_data['artist'], u'Aphex Twin')
        self.assertEqual(tag_data['album_artist'], u'Aphex Twin')
        self.assertEqual(tag_data['title'], u'Flap Head')
        self.assertEqual(tag_data['album'], u'Drukqs')
        self.assertEqual(tag_data['year'], u'2015')
        self.assertEqual(tag_data['trackno'], u'05/06')
        self.assertEqual(tag_data['discno'], u'01/01')
        self.assertEqual(tag_data['genre'], u'Electronic')
        self.assertEqual(tag_data['comment'], u'Nightwind Records (NW001)')

    def test__apply_artwork__cover_is_jpg__artwork_should_be_applied(self):
        tagger = FlacTagger()
        tagger.apply_artwork('tests/integration/data/cover.jpg', 'tests/integration/data/test_data.flac')
        artwork_data = get_flac_artwork_data('tests/integration/data/test_data.flac')
        size = os.path.getsize('tests/integration/data/cover.jpg')
        self.assertEqual('image/jpeg', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__cover_is_png__artwork_should_be_applied(self):
        tagger = FlacTagger()
        tagger.apply_artwork('tests/integration/data/cover.png', 'tests/integration/data/test_data.flac')
        artwork_data = get_flac_artwork_data('tests/integration/data/test_data.flac')
        size = os.path.getsize('tests/integration/data/cover.png')
        self.assertEqual('image/png', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__cover_is_jpeg__artwork_should_be_applied(self):
        tagger = FlacTagger()
        tagger.apply_artwork('tests/integration/data/cover.jpeg', 'tests/integration/data/test_data.flac')
        artwork_data = get_flac_artwork_data('tests/integration/data/test_data.flac')
        size = os.path.getsize('tests/integration/data/cover.jpeg')
        self.assertEqual('image/jpeg', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A cover art source must be supplied.'):
            tagger = FlacTagger()
            tagger.apply_artwork('', 'tests/integration/data/test_data.flac')

    def test__apply_artwork__destination_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A destination must be supplied to apply cover art to.'):
            tagger = FlacTagger()
            tagger.apply_artwork('tests/integration/data/cover.jpeg', '')

    def test__remove_tags__flac_has_tags__tags_are_removed(self):
        self.assertTrue(flac_has_tags('tests/integration/data/test_data_song_with_tags.flac'))
        tagger = FlacTagger()
        tagger.remove_tags('tests/integration/data/test_data_song_with_tags.flac')
        self.assertFalse(flac_has_tags('tests/integration/data/test_data_song_with_tags.flac'))

    def test__remove_tags__flac_has_no_tags__no_tags_are_added(self):
        tagger = FlacTagger()
        tagger.remove_tags('tests/integration/data/test_data.flac')
        self.assertFalse(flac_has_tags('tests/integration/data/test_data.flac'))

    def test__remove_tags__source_is_empty__no_tags_are_added(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be supplied.'):
            tagger = FlacTagger()
            tagger.remove_tags('')
