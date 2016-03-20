import os
import shutil
import unittest

import mock

from amu.audio import FlacTagger, TaggerError
from tests.helpers import get_flac_tag_data


class FlacTaggerTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.flac', 'tests/integration/data/test_data.flac')

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
