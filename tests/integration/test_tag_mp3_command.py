""" Test suite for the tag mp3 command. """
import mock
import os
import shutil
import unittest
from amu.commands import TagMp3Command
from amu.utils import get_id3_tag_data

class TagMp3CommandTest(unittest.TestCase):
    def setUp(self):
        shutil.copyfile('tests/integration/data/song.mp3', 'tests/integration/data/test_data.mp3')

    def tearDown(self):
        os.remove('tests/integration/data/test_data.mp3')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_id3_tag_on_the_mp3__mp3_should_have_correct_artist(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.artist = 'Aphex Twin'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['artist'], u'Aphex Twin')
