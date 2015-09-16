import mock
import os
import shutil
import unittest
from amu.audio import Mp3Tagger, TaggerError
from tests.helpers import get_mp3_artwork_data


class Mp3TaggerTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.mp3', 'tests/integration/data/test_data.mp3')

    def tearDown(self):
        os.remove('tests/integration/data/test_data.mp3')

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
