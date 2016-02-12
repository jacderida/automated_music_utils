import os
import shutil
import unittest
from amu.audio import FlacTagger


class FlacTaggerTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.flac', 'tests/integration/data/test_data.flac')

    def tearDown(self):
        os.remove('tests/integration/data/test_data.flac')

    def test__add_tags__source_is_empty__raises_value_error(self):
        with self.assertRaisesRegexp(ValueError, 'A source must be set for tagging a flac.'):
            tagger = FlacTagger()
            tagger.add_tags('')
