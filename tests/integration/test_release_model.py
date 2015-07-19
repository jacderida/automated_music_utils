import discogs_client
import unittest
from time import sleep
from amu.models import ReleaseModel

class ReleaseModelIntegrationTest(unittest.TestCase):
    def setUp(self):
        sleep(10)

    def test__from_discogs_release__release_with_single_artist_and_single_label__release_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'Aphex Twin')
        self.assertEqual(release.title, 'Selected Ambient Works 85-92')
        self.assertEqual(release.label, 'Apollo')
        self.assertEqual(release.catno, 'AMB3922RM')
        self.assertEqual(release.format, 'CD, Album, Remastered, Reissue')
        self.assertEqual(release.country, 'Belgium')
        self.assertEqual(release.year, '1992')
        self.assertEqual(release.genre, 'Electronic')

    def test__from_discogs_release__release_with_single_artist__tracklist_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(13, len(tracks))
        self.assertEqual(1, tracks[0].position)
        self.assertEqual('Xtal', tracks[0].title)
        self.assertEqual(2, tracks[1].position)
        self.assertEqual('Tha', tracks[1].title)
        self.assertEqual(3, tracks[2].position)
        self.assertEqual('Pulsewidth', tracks[2].title)
        self.assertEqual(4, tracks[3].position)
        self.assertEqual('Ageispolis', tracks[3].title)
        self.assertEqual(5, tracks[4].position)
        self.assertEqual('i', tracks[4].title)
        self.assertEqual(6, tracks[5].position)
        self.assertEqual('Green Calx', tracks[5].title)
        self.assertEqual(7, tracks[6].position)
        self.assertEqual('Heliosphan', tracks[6].title)
        self.assertEqual(8, tracks[7].position)
        self.assertEqual('We Are The Music Makers', tracks[7].title)
        self.assertEqual(9, tracks[8].position)
        self.assertEqual('Schottkey 7th Path', tracks[8].title)
        self.assertEqual(10, tracks[9].position)
        self.assertEqual('Ptolemy', tracks[9].title)
        self.assertEqual(11, tracks[10].position)
        self.assertEqual('Hedphelym', tracks[10].title)
        self.assertEqual(12, tracks[11].position)
        self.assertEqual('Delphium', tracks[11].title)
        self.assertEqual(13, tracks[12].position)
        self.assertEqual('Actium', tracks[12].title)

    def test__from_discogs_release__release_with_single_disc__disc_number_and_total_are_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(1, tracks[0].disc_number)
        self.assertEqual(1, tracks[0].disc_total)
        self.assertEqual(1, tracks[1].disc_number)
        self.assertEqual(1, tracks[1].disc_total)
        self.assertEqual(1, tracks[2].disc_number)
        self.assertEqual(1, tracks[2].disc_total)
        self.assertEqual(1, tracks[3].disc_number)
        self.assertEqual(1, tracks[3].disc_total)
        self.assertEqual(1, tracks[4].disc_number)
        self.assertEqual(1, tracks[4].disc_total)
        self.assertEqual(1, tracks[5].disc_number)
        self.assertEqual(1, tracks[5].disc_total)
        self.assertEqual(1, tracks[6].disc_number)
        self.assertEqual(1, tracks[6].disc_total)
        self.assertEqual(1, tracks[7].disc_number)
        self.assertEqual(1, tracks[7].disc_total)
        self.assertEqual(1, tracks[8].disc_number)
        self.assertEqual(1, tracks[8].disc_total)
        self.assertEqual(1, tracks[9].disc_number)
        self.assertEqual(1, tracks[9].disc_total)
        self.assertEqual(1, tracks[10].disc_number)
        self.assertEqual(1, tracks[10].disc_total)
        self.assertEqual(1, tracks[11].disc_number)
        self.assertEqual(1, tracks[11].disc_total)
        self.assertEqual(1, tracks[12].disc_number)
        self.assertEqual(1, tracks[12].disc_total)

    def test__from_discogs_release__release_with_multiple_discs__disc_number_and_total_are_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(127710)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(1, tracks[0].disc_number)
        self.assertEqual(2, tracks[0].disc_total)
        self.assertEqual(1, tracks[1].disc_number)
        self.assertEqual(2, tracks[1].disc_total)
        self.assertEqual(1, tracks[2].disc_number)
        self.assertEqual(2, tracks[2].disc_total)
        self.assertEqual(1, tracks[3].disc_number)
        self.assertEqual(2, tracks[3].disc_total)
        self.assertEqual(1, tracks[4].disc_number)
        self.assertEqual(2, tracks[4].disc_total)
        self.assertEqual(1, tracks[5].disc_number)
        self.assertEqual(2, tracks[5].disc_total)
        self.assertEqual(1, tracks[6].disc_number)
        self.assertEqual(2, tracks[6].disc_total)
        self.assertEqual(1, tracks[7].disc_number)
        self.assertEqual(2, tracks[7].disc_total)
        self.assertEqual(1, tracks[8].disc_number)
        self.assertEqual(2, tracks[8].disc_total)
        self.assertEqual(1, tracks[9].disc_number)
        self.assertEqual(2, tracks[9].disc_total)
        self.assertEqual(1, tracks[10].disc_number)
        self.assertEqual(2, tracks[10].disc_total)
        self.assertEqual(1, tracks[11].disc_number)
        self.assertEqual(2, tracks[11].disc_total)
        self.assertEqual(1, tracks[12].disc_number)
        self.assertEqual(2, tracks[12].disc_total)
        self.assertEqual(2, tracks[13].disc_number)
        self.assertEqual(2, tracks[13].disc_total)
        self.assertEqual(2, tracks[14].disc_number)
        self.assertEqual(2, tracks[14].disc_total)
        self.assertEqual(2, tracks[15].disc_number)
        self.assertEqual(2, tracks[15].disc_total)
        self.assertEqual(2, tracks[16].disc_number)
        self.assertEqual(2, tracks[16].disc_total)
        self.assertEqual(2, tracks[17].disc_number)
        self.assertEqual(2, tracks[17].disc_total)
        self.assertEqual(2, tracks[18].disc_number)
        self.assertEqual(2, tracks[18].disc_total)
        self.assertEqual(2, tracks[19].disc_number)
        self.assertEqual(2, tracks[19].disc_total)
        self.assertEqual(2, tracks[20].disc_number)
        self.assertEqual(2, tracks[20].disc_total)
        self.assertEqual(2, tracks[21].disc_number)
        self.assertEqual(2, tracks[21].disc_total)
        self.assertEqual(2, tracks[22].disc_number)
        self.assertEqual(2, tracks[22].disc_total)
        self.assertEqual(2, tracks[23].disc_number)
        self.assertEqual(2, tracks[23].disc_total)
        self.assertEqual(2, tracks[24].disc_number)
        self.assertEqual(2, tracks[24].disc_total)
        self.assertEqual(2, tracks[25].disc_number)
        self.assertEqual(2, tracks[25].disc_total)

    def test__from_discogs_release__vinyl_release_with_multiple_records__disc_number_and_total_are_set_to_1(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(55036)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(1, tracks[0].disc_number)
        self.assertEqual(1, tracks[0].disc_total)
        self.assertEqual(1, tracks[1].disc_number)
        self.assertEqual(1, tracks[1].disc_total)
        self.assertEqual(1, tracks[2].disc_number)
        self.assertEqual(1, tracks[2].disc_total)
        self.assertEqual(1, tracks[3].disc_number)
        self.assertEqual(1, tracks[3].disc_total)
        self.assertEqual(1, tracks[4].disc_number)
        self.assertEqual(1, tracks[4].disc_total)
        self.assertEqual(1, tracks[5].disc_number)
        self.assertEqual(1, tracks[5].disc_total)
        self.assertEqual(1, tracks[6].disc_number)
        self.assertEqual(1, tracks[6].disc_total)
        self.assertEqual(1, tracks[7].disc_number)
        self.assertEqual(1, tracks[7].disc_total)

    def test__from_discogs_release__release_is_multi_cd_with_hyphen_disc_track_number_separator__tracklist_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(3636)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(24, len(tracks))
        self.assertEqual(1, tracks[0].position)
        self.assertEqual('Untitled', tracks[0].title)
        self.assertEqual(2, tracks[1].position)
        self.assertEqual('Untitled', tracks[1].title)
        self.assertEqual(3, tracks[2].position)
        self.assertEqual('Untitled', tracks[2].title)
        self.assertEqual(4, tracks[3].position)
        self.assertEqual('Untitled', tracks[3].title)
        self.assertEqual(5, tracks[4].position)
        self.assertEqual('Untitled', tracks[4].title)
        self.assertEqual(6, tracks[5].position)
        self.assertEqual('Untitled', tracks[5].title)
        self.assertEqual(7, tracks[6].position)
        self.assertEqual('Untitled', tracks[6].title)
        self.assertEqual(8, tracks[7].position)
        self.assertEqual('Untitled', tracks[7].title)
        self.assertEqual(9, tracks[8].position)
        self.assertEqual('Untitled', tracks[8].title)
        self.assertEqual(10, tracks[9].position)
        self.assertEqual('Untitled', tracks[9].title)
        self.assertEqual(11, tracks[10].position)
        self.assertEqual('Untitled', tracks[10].title)
        self.assertEqual(12, tracks[11].position)
        self.assertEqual('Untitled', tracks[11].title)
        self.assertEqual(1, tracks[12].position)
        self.assertEqual('Blue Calx', tracks[12].title)
        self.assertEqual(2, tracks[13].position)
        self.assertEqual('Untitled', tracks[13].title)
        self.assertEqual(3, tracks[14].position)
        self.assertEqual('Untitled', tracks[14].title)
        self.assertEqual(4, tracks[15].position)
        self.assertEqual('Untitled', tracks[15].title)
        self.assertEqual(5, tracks[16].position)
        self.assertEqual('Untitled', tracks[16].title)
        self.assertEqual(6, tracks[17].position)
        self.assertEqual('Untitled', tracks[17].title)
        self.assertEqual(7, tracks[18].position)
        self.assertEqual('Untitled', tracks[18].title)
        self.assertEqual(8, tracks[19].position)
        self.assertEqual('Untitled', tracks[19].title)
        self.assertEqual(9, tracks[20].position)
        self.assertEqual('Untitled', tracks[20].title)
        self.assertEqual(10, tracks[21].position)
        self.assertEqual('Untitled', tracks[21].title)
        self.assertEqual(11, tracks[22].position)
        self.assertEqual('Untitled', tracks[22].title)
        self.assertEqual(12, tracks[23].position)
        self.assertEqual('Untitled', tracks[23].title)

    def test__from_discogs_release__release_is_a_reissue__release_year_from_master_is_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.year, '1992')

    def test__from_discogs_release__release_artist_is_anv__anv_is_resolved(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(28763)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'AFX')

    def test__from_discogs_release__release_has_artists_with_multiple_anvs__anvs_are_resolved(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(2679310)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'W. Bennett / B. Bennett')

    def test__from_discogs_release__release_has_multiple_artists__the_joined_artist_is_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(202433)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'Aphex Twin / Gavin Bryars')

    def test__from_discogs_release__release_has_no_master__the_date_for_the_current_release_is_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(202433)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.year, '1995')

    def test__from_discogs_release__release_has_multiple_genres__the_full_list_of_genres_are_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1952653)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.genre, 'Electronic, Stage & Screen')

    def test__from_discogs_release__release_has_multiple_labels__the_full_list_of_labels_are_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(2318107)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.label, 'Apollo, [PIAS] Recordings')

    def test__from_discogs_release__release_has_multiple_labels__the_full_list_of_catnos_are_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(2318107)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.catno, 'AMB3922CD, 516.9522.020')

    def test__from_discogs_release__release_has_artists_separated_by_commas__the_correct_joined_artist_is_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(6517290)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.artist, 'Jack Jezioro, Craig Duncan, John Dockery')

    def test__from_discogs_release__release_has_no_date__unknown_is_used_as_date_string(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(3709896)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.year, 'Unknown')

    def test__from_discogs_release__release_has_index_tracks__index_tracks_should_be_ignored(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(804556)
        discogs_release.refresh()
        tracks = ReleaseModel.from_discogs_release(discogs_release).get_tracks()
        self.assertEqual(len(tracks), 15)

    def test__from_discogs_release__release_has_artists_on_tracks__the_tracks_should_have_artists_assigned(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(480352)
        discogs_release.refresh()
        tracks = ReleaseModel.from_discogs_release(discogs_release).get_tracks()
        self.assertEqual('Franck Sarrio', tracks[0].artist)
        self.assertEqual('Subliminal Criminal', tracks[1].artist)
        self.assertEqual('AU', tracks[2].artist)
        self.assertEqual('Duracel', tracks[3].artist)
        self.assertEqual('Nimoy (2)', tracks[4].artist)
        self.assertEqual('Syncom Data', tracks[5].artist)
        self.assertEqual('Rude 66', tracks[6].artist)
        self.assertEqual('Hank (32)', tracks[7].artist)

    def test__from_discogs_release__release_has_artists_on_tracks_with_anvs__the_anvs_should_be_resolved(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(51236)
        discogs_release.refresh()
        tracks = ReleaseModel.from_discogs_release(discogs_release).get_tracks()
        self.assertEqual('Red Cell', tracks[3].artist)
        self.assertEqual('Neuro Politique', tracks[4].artist)
        self.assertEqual('Kosmik Kommando', tracks[5].artist)

    def test__from_discogs_release__release_has_artists_on_tracks_with_joins__the_artists_should_be_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(56042)
        discogs_release.refresh()
        tracks = ReleaseModel.from_discogs_release(discogs_release).get_tracks()
        self.assertEqual('Overdose / Duracel', tracks[2].artist)
