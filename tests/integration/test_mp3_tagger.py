import mock
import os
import shutil
import unittest
from amu.audio import Mp3Tagger, TaggerError
from amu.utils import get_id3_tag_data
from tests.helpers import get_mp3_artwork_data
from tests.helpers import mp3_has_tags


class Mp3TaggerTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.mp3', 'tests/integration/data/test_data.mp3')
        shutil.copyfile('tests/integration/data/song_with_only_id3v1_tags.mp3', 'tests/integration/data/copy_of_song_with_only_id3v1_tags.mp3')
        shutil.copyfile('tests/integration/data/song_with_only_id3v2_tags.mp3', 'tests/integration/data/copy_of_song_with_only_id3v2_tags.mp3')
        shutil.copyfile('tests/integration/data/song_with_both_id3v2_and_id3v1_tags.mp3', 'tests/integration/data/copy_of_song_with_both_id3v2_and_id3v1_tags.mp3')

    def tearDown(self):
        os.remove('tests/integration/data/test_data.mp3')
        os.remove('tests/integration/data/copy_of_song_with_only_id3v1_tags.mp3')
        os.remove('tests/integration/data/copy_of_song_with_only_id3v2_tags.mp3')
        os.remove('tests/integration/data/copy_of_song_with_both_id3v2_and_id3v1_tags.mp3')

    def test__add_tags__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be set for tagging an mp3.'):
            tagger = Mp3Tagger()
            tagger.add_tags('')

    @mock.patch('os.path.exists')
    def test__add_tags__source_does_not_exist__raises_tagger_error(self, exists_mock):
        exists_mock.return_value = False
        with self.assertRaisesRegexp(TaggerError, 'The source /some/non/existent/mp3 does not exist.'):
            tagger = Mp3Tagger()
            tagger.add_tags('/some/non/existent/mp3')

    @mock.patch('os.path.isdir')
    @mock.patch('os.path.exists')
    def test__add_tags__source_is_directory__raises_tagger_error(self, exists_mock, isdir_mock):
        exists_mock.return_value = True
        isdir_mock.return_value = True
        with self.assertRaisesRegexp(TaggerError, 'The source must not be a directory.'):
            tagger = Mp3Tagger()
            tagger.add_tags('/some/non/existent/mp3')

    def test__add_tags__artist_is_set__tag_should_have_an_artist_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', artist='Aphex Twin')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['artist'], u'Aphex Twin')

    def test__add_tags__artist_is_not_set__artist_should_be_set_to_placeholder(self):
        # It's horrible to have to check for this placeholder value, but due to the way
        # the tagging library works, sadly it's necessary.
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['artist'], u'placeholder')

    def test__add_tags__album_artist_is_set__tag_should_have_an_album_artist_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', album_artist='Various')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['album_artist'], u'Various')

    def test__add_tags__album_artist_is_not_set__tag_should_not_have_an_album_artist_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('album_artist'))

    def test__add_tags__title_is_set__tag_should_have_a_title_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', title='Flap Head')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['title'], u'Flap Head')

    def test__add_tags__title_is_not_set__tag_should_not_have_a_title_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('title'))

    def test__add_tags__album_is_set__tag_should_have_an_album_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', album='Dark Side of the Moon')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['album'], u'Dark Side of the Moon')

    def test__add_tags__album_is_not_set__tag_should_not_have_an_album_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('album'))

    def test__add_tags__year_is_set__tag_should_have_a_year_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', year='2015')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['year'], u'2015')

    def test__add_tags__year_is_not_set__tag_should_not_have_a_year_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('year'))

    def test__add_tags__genre_is_set__tag_should_have_a_genre_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', genre='Electronic')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['genre'], u'Electronic')

    def test__add_tags__genre_is_not_set__tag_should_not_have_a_genre_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('genre'))

    def test__add_tags__comment_is_set__tag_should_have_a_comment_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', comment='WARPCD92')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['comment'], u'WARPCD92')

    def test__add_tags__comment_is_not_set__tag_should_not_have_a_comment_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3')
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertFalse(tag_data.has_key('comment'))

    def test__add_tags__track_number_is_set__tag_should_have_a_track_number_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', track_number=10, track_total=15)
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'10/15')

    def test__add_tags__track_number_is_less_than_10__tag_should_have_a_padded_track_number_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', track_number=5, track_total=15)
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'05/15')

    def test__add_tags__track_total_is_less_than_10__tag_should_have_a_padded_track_total_frame(self):
        tagger = Mp3Tagger()
        tagger.add_tags('tests/integration/data/test_data.mp3', track_number=5, track_total=6)
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'05/06')

    def test__apply_artwork__cover_is_jpg__artwork_should_be_applied(self):
        tagger = Mp3Tagger()
        tagger.apply_artwork('tests/integration/data/cover.jpg', 'tests/integration/data/test_data.mp3')
        artwork_data = get_mp3_artwork_data('tests/integration/data/test_data.mp3')
        size = os.path.getsize('tests/integration/data/cover.jpg')
        self.assertEqual('image/jpeg', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__cover_is_png__artwork_should_be_applied(self):
        tagger = Mp3Tagger()
        tagger.apply_artwork('tests/integration/data/cover.png', 'tests/integration/data/test_data.mp3')
        artwork_data = get_mp3_artwork_data('tests/integration/data/test_data.mp3')
        size = os.path.getsize('tests/integration/data/cover.png')
        self.assertEqual('image/png', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__cover_is_jpeg__artwork_should_be_applied(self):
        tagger = Mp3Tagger()
        tagger.apply_artwork('tests/integration/data/cover.jpeg', 'tests/integration/data/test_data.mp3')
        artwork_data = get_mp3_artwork_data('tests/integration/data/test_data.mp3')
        size = os.path.getsize('tests/integration/data/cover.jpeg')
        self.assertEqual('image/jpeg', artwork_data[0])
        self.assertEqual(size, artwork_data[1])

    def test__apply_artwork__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A cover art source must be supplied.'):
            tagger = Mp3Tagger()
            tagger.apply_artwork('', 'tests/integration/data/test_data.mp3')

    def test__apply_artwork__destination_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A destination must be supplied to apply cover art to.'):
            tagger = Mp3Tagger()
            tagger.apply_artwork('tests/integration/data/cover.jpg', '')

    def test__apply_artwork__source_does_not_exist__raises_tagger_error(self):
        with self.assertRaisesRegexp(TaggerError, 'The cover art source does not exist.'):
            tagger = Mp3Tagger()
            tagger.apply_artwork('/some/non/existent/source.jpg', 'tests/integration/data/test_data.mp3')

    def test__apply_artwork__destination_does_not_exist__raises_tagger_error(self):
        with self.assertRaisesRegexp(TaggerError, 'The cover art destination does not exist.'):
            tagger = Mp3Tagger()
            tagger.apply_artwork('tests/integration/data/cover.jpg', '/some/non/existent/destination.mp3')

    @mock.patch('os.path.exists')
    def test__apply_artwork__destination_is_not_mp3__raises_tagger_error(self, exists_mock):
        with self.assertRaisesRegexp(TaggerError, 'The destination must be an mp3.'):
            exists_mock.side_effect = [True, True]
            tagger = Mp3Tagger()
            tagger.apply_artwork('tests/integration/data/cover.jpg', '/some/non/existent/destination.flac')

    def test__remove_tags__mp3_has_only_id3v1_tag__id3v1_tag_is_removed(self):
        source = 'tests/integration/data/copy_of_song_with_only_id3v1_tags.mp3'
        tagger = Mp3Tagger()
        tagger.remove_tags(source)
        self.assertFalse(mp3_has_tags(source))

    def test__remove_tags__mp3_has_only_id3v2_tag__id3v2_tag_is_removed(self):
        source = 'tests/integration/data/copy_of_song_with_only_id3v2_tags.mp3'
        tagger = Mp3Tagger()
        tagger.remove_tags(source)
        self.assertFalse(mp3_has_tags(source))

    def test__remove_tags__mp3_has_both_id3v2_and_id3v1_tags__both_tags_are_removed(self):
        source = 'tests/integration/data/copy_of_song_with_both_id3v2_and_id3v1_tags.mp3'
        tagger = Mp3Tagger()
        tagger.remove_tags(source)
        self.assertFalse(mp3_has_tags(source))

    def test__remove_tags__mp3_has_no_tags__no_error_should_be_raised_and_no_tags_should_be_applied(self):
        source = 'tests/integration/data/test_data.mp3'
        tagger = Mp3Tagger()
        tagger.remove_tags(source)
        self.assertFalse(mp3_has_tags(source))
