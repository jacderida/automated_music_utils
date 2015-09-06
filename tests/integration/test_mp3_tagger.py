import mock
import os
import shutil
import unittest
from amu.audio import Mp3Tagger
from amu.utils import get_id3_tag_data
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
