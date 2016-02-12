import os
import shutil
import unittest

import mock

from amu.audio import FlacTagger, TaggerError


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
