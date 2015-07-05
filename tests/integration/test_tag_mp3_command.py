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
    def test__execute__set_the_artist_on_the_id3_tag__tag_should_have_correct_artist(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.artist = 'Aphex Twin'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['artist'], u'Aphex Twin')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_title_on_the_id3_tag__tag_should_have_correct_title(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.title = 'Flap Head'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['title'], u'Flap Head')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_album_on_the_id3_tag__tag_should_have_correct_album(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.album = 'Drukqs'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['album'], u'Drukqs')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_year_on_the_id3_tag__tag_should_have_correct_year(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.year = '2015'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['year'], u'2015')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_track_number_on_the_id3_tag__tag_should_have_correct_track_number(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.track_number = 10
        command.track_total = 15
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'10/15')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__track_number_is_less_than_10__tag_should_have_correct_track_number_padded_with_0(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.track_number = 5
        command.track_total = 15
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'05/15')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__track_total_is_less_than_10__tag_should_have_correct_track_total_padded_with_0(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.track_number = 5
        command.track_total = 6
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['trackno'], u'05/06')

    @mock.patch('amu.config.ConfigurationProvider')
    def test__execute__set_the_genre_on_the_id3_tag__tag_should_have_correct_genre(self, config_mock):
        command = TagMp3Command(config_mock)
        command.source = 'tests/integration/data/test_data.mp3'
        command.genre = 'Techno'
        command.execute()
        tag_data = get_id3_tag_data('tests/integration/data/test_data.mp3')
        self.assertEqual(tag_data['genre'], u'Techno')
