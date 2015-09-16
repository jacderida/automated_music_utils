import discogs_client
import unittest
from time import sleep
from amu.models import ReleaseModel

class ReleaseModelIntegrationTest(unittest.TestCase):
    def tearDown(self):
        sleep(2)

    def test__from_discogs_release__release_with_single_artist_and_single_label__release_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.discogs_id, 1303737)
        self.assertEqual(release.artist, 'Aphex Twin')
        self.assertEqual(release.title, 'Selected Ambient Works 85-92')
        self.assertEqual(release.label, 'Apollo')
        self.assertEqual(release.catno, 'AMB3922RM')
        self.assertEqual(release.format, 'CD, Album, Reissue, Remastered')
        self.assertEqual(release.country, 'Belgium')
        self.assertEqual(release.original_year, '1992')
        self.assertEqual(release.year, '2008')
        self.assertEqual(release.genre, 'Electronic')

    def test__from_discogs_release__release_has_single_disc__the_track_number_and_totals_should_be_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(1, tracks[0].track_number)
        self.assertEqual(13, tracks[0].track_total)
        self.assertEqual(2, tracks[1].track_number)
        self.assertEqual(13, tracks[1].track_total)
        self.assertEqual(3, tracks[2].track_number)
        self.assertEqual(13, tracks[2].track_total)
        self.assertEqual(4, tracks[3].track_number)
        self.assertEqual(13, tracks[3].track_total)
        self.assertEqual(5, tracks[4].track_number)
        self.assertEqual(13, tracks[4].track_total)
        self.assertEqual(6, tracks[5].track_number)
        self.assertEqual(13, tracks[5].track_total)
        self.assertEqual(7, tracks[6].track_number)
        self.assertEqual(13, tracks[6].track_total)
        self.assertEqual(8, tracks[7].track_number)
        self.assertEqual(13, tracks[7].track_total)
        self.assertEqual(9, tracks[8].track_number)
        self.assertEqual(13, tracks[8].track_total)
        self.assertEqual(10, tracks[9].track_number)
        self.assertEqual(13, tracks[9].track_total)
        self.assertEqual(11, tracks[10].track_number)
        self.assertEqual(13, tracks[10].track_total)
        self.assertEqual(12, tracks[11].track_number)
        self.assertEqual(13, tracks[11].track_total)
        self.assertEqual(13, tracks[12].track_number)
        self.assertEqual(13, tracks[12].track_total)

    def test__from_discogs_release__release_with_single_artist__tracklist_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(13, len(tracks))
        self.assertEqual('Xtal', tracks[0].title)
        self.assertEqual('Tha', tracks[1].title)
        self.assertEqual('Pulsewidth', tracks[2].title)
        self.assertEqual('Ageispolis', tracks[3].title)
        self.assertEqual('i', tracks[4].title)
        self.assertEqual('Green Calx', tracks[5].title)
        self.assertEqual('Heliosphan', tracks[6].title)
        self.assertEqual('We Are The Music Makers', tracks[7].title)
        self.assertEqual('Schottkey 7th Path', tracks[8].title)
        self.assertEqual('Ptolemy', tracks[9].title)
        self.assertEqual('Hedphelym', tracks[10].title)
        self.assertEqual('Delphium', tracks[11].title)
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
        self.assertEqual(1, tracks[0].track_number)
        self.assertEqual(12, tracks[0].track_total)
        self.assertEqual('Untitled', tracks[0].title)
        self.assertEqual(2, tracks[1].track_number)
        self.assertEqual(12, tracks[1].track_total)
        self.assertEqual('Untitled', tracks[1].title)
        self.assertEqual(3, tracks[2].track_number)
        self.assertEqual(12, tracks[2].track_total)
        self.assertEqual('Untitled', tracks[2].title)
        self.assertEqual(4, tracks[3].track_number)
        self.assertEqual(12, tracks[3].track_total)
        self.assertEqual('Untitled', tracks[3].title)
        self.assertEqual(5, tracks[4].track_number)
        self.assertEqual(12, tracks[4].track_total)
        self.assertEqual('Untitled', tracks[4].title)
        self.assertEqual(6, tracks[5].track_number)
        self.assertEqual(12, tracks[5].track_total)
        self.assertEqual('Untitled', tracks[5].title)
        self.assertEqual(7, tracks[6].track_number)
        self.assertEqual(12, tracks[6].track_total)
        self.assertEqual('Untitled', tracks[6].title)
        self.assertEqual(8, tracks[7].track_number)
        self.assertEqual(12, tracks[7].track_total)
        self.assertEqual('Untitled', tracks[7].title)
        self.assertEqual(9, tracks[8].track_number)
        self.assertEqual(12, tracks[8].track_total)
        self.assertEqual('Untitled', tracks[8].title)
        self.assertEqual(10, tracks[9].track_number)
        self.assertEqual(12, tracks[9].track_total)
        self.assertEqual('Untitled', tracks[9].title)
        self.assertEqual(11, tracks[10].track_number)
        self.assertEqual(12, tracks[10].track_total)
        self.assertEqual('Untitled', tracks[10].title)
        self.assertEqual(12, tracks[11].track_number)
        self.assertEqual(12, tracks[11].track_total)
        self.assertEqual('Untitled', tracks[11].title)
        self.assertEqual(1, tracks[12].track_number)
        self.assertEqual(12, tracks[12].track_total)
        self.assertEqual('Blue Calx', tracks[12].title)
        self.assertEqual(2, tracks[13].track_number)
        self.assertEqual(12, tracks[13].track_total)
        self.assertEqual('Untitled', tracks[13].title)
        self.assertEqual(3, tracks[14].track_number)
        self.assertEqual(12, tracks[14].track_total)
        self.assertEqual('Untitled', tracks[14].title)
        self.assertEqual(4, tracks[15].track_number)
        self.assertEqual(12, tracks[15].track_total)
        self.assertEqual('Untitled', tracks[15].title)
        self.assertEqual(5, tracks[16].track_number)
        self.assertEqual(12, tracks[16].track_total)
        self.assertEqual('Untitled', tracks[16].title)
        self.assertEqual(6, tracks[17].track_number)
        self.assertEqual(12, tracks[17].track_total)
        self.assertEqual('Untitled', tracks[17].title)
        self.assertEqual(7, tracks[18].track_number)
        self.assertEqual(12, tracks[18].track_total)
        self.assertEqual('Untitled', tracks[18].title)
        self.assertEqual(8, tracks[19].track_number)
        self.assertEqual(12, tracks[19].track_total)
        self.assertEqual('Untitled', tracks[19].title)
        self.assertEqual(9, tracks[20].track_number)
        self.assertEqual(12, tracks[20].track_total)
        self.assertEqual('Untitled', tracks[20].title)
        self.assertEqual(10, tracks[21].track_number)
        self.assertEqual(12, tracks[21].track_total)
        self.assertEqual('Untitled', tracks[21].title)
        self.assertEqual(11, tracks[22].track_number)
        self.assertEqual(12, tracks[22].track_total)
        self.assertEqual('Untitled', tracks[22].title)
        self.assertEqual(12, tracks[23].track_number)
        self.assertEqual(12, tracks[23].track_total)
        self.assertEqual('Untitled', tracks[23].title)

    def test__from_discogs_release__release_is_multi_cd_with_dot_disc_track_number_separator__tracklist_is_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(3516145)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release.get_tracks()
        self.assertEqual(37, len(tracks))
        self.assertEqual(1, tracks[0].track_number)
        self.assertEqual(19, tracks[0].track_total)
        self.assertEqual('Just For You (Excerpt 1)', tracks[0].title)
        self.assertEqual(2, tracks[1].track_number)
        self.assertEqual(19, tracks[1].track_total)
        self.assertEqual('Eton', tracks[1].title)
        self.assertEqual(3, tracks[2].track_number)
        self.assertEqual(19, tracks[2].track_total)
        self.assertEqual('The Innocents - Savage Noises (Excerpt) (1961)', tracks[2].title)
        self.assertEqual(4, tracks[3].track_number)
        self.assertEqual(19, tracks[3].track_total)
        self.assertEqual('Anchor Butter', tracks[3].title)
        self.assertEqual(5, tracks[4].track_number)
        self.assertEqual(19, tracks[4].track_total)
        self.assertEqual('Wool (1967)', tracks[4].title)
        self.assertEqual(6, tracks[5].track_number)
        self.assertEqual(19, tracks[5].track_total)
        self.assertEqual('Oxford', tracks[5].title)
        self.assertEqual(7, tracks[6].track_number)
        self.assertEqual(19, tracks[6].track_total)
        self.assertEqual('Hydrogen Tones', tracks[6].title)
        self.assertEqual(8, tracks[7].track_number)
        self.assertEqual(19, tracks[7].track_total)
        self.assertEqual('2001 Effects Tape 1', tracks[7].title)
        self.assertEqual(9, tracks[8].track_number)
        self.assertEqual(19, tracks[8].track_total)
        self.assertEqual('2001 Effects Tape 2', tracks[8].title)
        self.assertEqual(10, tracks[9].track_number)
        self.assertEqual(19, tracks[9].track_total)
        self.assertEqual('Phensic (1961)', tracks[9].title)
        self.assertEqual(11, tracks[10].track_number)
        self.assertEqual(19, tracks[10].track_total)
        self.assertEqual('New Atlantis (1963)', tracks[10].title)
        self.assertEqual(12, tracks[11].track_number)
        self.assertEqual(19, tracks[11].track_total)
        self.assertEqual('Just For You (Excerpt 2)', tracks[11].title)
        self.assertEqual(13, tracks[12].track_number)
        self.assertEqual(19, tracks[12].track_total)
        self.assertEqual('Winters Journey (Intro) (1958)', tracks[12].title)
        self.assertEqual(14, tracks[13].track_number)
        self.assertEqual(19, tracks[13].track_total)
        self.assertEqual('Pulse Persephone (Alternate Parts For Mixing)', tracks[13].title)
        self.assertEqual(15, tracks[14].track_number)
        self.assertEqual(19, tracks[14].track_total)
        self.assertEqual('Light Music (Excerpt)', tracks[14].title)
        self.assertEqual(16, tracks[15].track_number)
        self.assertEqual(19, tracks[15].track_total)
        self.assertEqual('Stroke', tracks[15].title)
        self.assertEqual(17, tracks[16].track_number)
        self.assertEqual(19, tracks[16].track_total)
        self.assertEqual('Shell Flight (Excerpt)', tracks[16].title)
        self.assertEqual(18, tracks[17].track_number)
        self.assertEqual(19, tracks[17].track_total)
        self.assertEqual('Anacin Components', tracks[17].title)
        self.assertEqual(19, tracks[18].track_number)
        self.assertEqual(19, tracks[18].track_total)
        self.assertEqual('G.O.S. (Excerpt - 15" Tape Transferred At 7.5" Ps)', tracks[18].title)
        self.assertEqual(1, tracks[19].track_number)
        self.assertEqual(18, tracks[19].track_total)
        self.assertEqual('Costain Outtake', tracks[19].title)
        self.assertEqual(2, tracks[20].track_number)
        self.assertEqual(18, tracks[20].track_total)
        self.assertEqual('Encephalagraph', tracks[20].title)
        self.assertEqual(3, tracks[21].track_number)
        self.assertEqual(18, tracks[21].track_total)
        self.assertEqual('Anacin (Excerpt)', tracks[21].title)
        self.assertEqual(4, tracks[22].track_number)
        self.assertEqual(18, tracks[22].track_total)
        self.assertEqual('Hamlet - Youth Theatre (1963)', tracks[22].title)
        self.assertEqual(5, tracks[23].track_number)
        self.assertEqual(18, tracks[23].track_total)
        self.assertEqual('For Granada (1967)', tracks[23].title)
        self.assertEqual(6, tracks[24].track_number)
        self.assertEqual(18, tracks[24].track_total)
        self.assertEqual('Oramics Demonstration (Excerpt)', tracks[24].title)
        self.assertEqual(7, tracks[25].track_number)
        self.assertEqual(18, tracks[25].track_total)
        self.assertEqual('Electronic Sound Patterns (Excerpt) (1962)', tracks[25].title)
        self.assertEqual(8, tracks[26].track_number)
        self.assertEqual(18, tracks[26].track_total)
        self.assertEqual('Pure Tone Excerpts', tracks[26].title)
        self.assertEqual(9, tracks[27].track_number)
        self.assertEqual(18, tracks[27].track_total)
        self.assertEqual('Hospital', tracks[27].title)
        self.assertEqual(10, tracks[28].track_number)
        self.assertEqual(18, tracks[28].track_total)
        self.assertEqual('Mermaid (Excerpt)', tracks[28].title)
        self.assertEqual(11, tracks[29].track_number)
        self.assertEqual(18, tracks[29].track_total)
        self.assertEqual('Shell', tracks[29].title)
        self.assertEqual(12, tracks[30].track_number)
        self.assertEqual(18, tracks[30].track_total)
        self.assertEqual('Illustrations (Fireworks / Hardwich High School) (1967)', tracks[30].title)
        self.assertEqual(13, tracks[31].track_number)
        self.assertEqual(18, tracks[31].track_total)
        self.assertEqual('Ursa Major (Sun Mix) (1962)', tracks[31].title)
        self.assertEqual(14, tracks[32].track_number)
        self.assertEqual(18, tracks[32].track_total)
        self.assertEqual('Oddments (Excerpt)', tracks[32].title)
        self.assertEqual(15, tracks[33].track_number)
        self.assertEqual(18, tracks[33].track_total)
        self.assertEqual('Osram & Rank / Pulse Persephone Experiment (1963)', tracks[33].title)
        self.assertEqual(16, tracks[34].track_number)
        self.assertEqual(18, tracks[34].track_total)
        self.assertEqual('Pulse Persephone Pitch Experiment (1963)', tracks[34].title)
        self.assertEqual(17, tracks[35].track_number)
        self.assertEqual(18, tracks[35].track_total)
        self.assertEqual('Sardonica (Excerpt)', tracks[35].title)
        self.assertEqual(18, tracks[36].track_number)
        self.assertEqual(18, tracks[36].track_total)
        self.assertEqual('Barclays Bank (Excerpt)', tracks[36].title)

    def test__from_discogs_release__release_is_a_reissue__original_year_and_release_year_are_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1303737)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.original_year, '1992')
        self.assertEqual(release.year, '2008')

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

    def test__from_discogs_release__release_has_no_master__original_year_and_release_year_are_assigned_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(202433)
        discogs_release.refresh()
        release = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release.year, '1995')
        self.assertEqual(release.original_year, '1995')

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

    def test__from_discogs_release__release_has_index_tracks__correct_track_totals_should_be_used(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(804556)
        discogs_release.refresh()
        tracks = ReleaseModel.from_discogs_release(discogs_release).get_tracks()
        self.assertEqual(1, tracks[0].track_number)
        self.assertEqual(15, tracks[0].track_total)
        self.assertEqual(2, tracks[1].track_number)
        self.assertEqual(15, tracks[1].track_total)
        self.assertEqual(3, tracks[2].track_number)
        self.assertEqual(15, tracks[2].track_total)
        self.assertEqual(4, tracks[3].track_number)
        self.assertEqual(15, tracks[3].track_total)
        self.assertEqual(5, tracks[4].track_number)
        self.assertEqual(15, tracks[4].track_total)
        self.assertEqual(6, tracks[5].track_number)
        self.assertEqual(15, tracks[5].track_total)
        self.assertEqual(7, tracks[6].track_number)
        self.assertEqual(15, tracks[6].track_total)
        self.assertEqual(8, tracks[7].track_number)
        self.assertEqual(15, tracks[7].track_total)
        self.assertEqual(9, tracks[8].track_number)
        self.assertEqual(15, tracks[8].track_total)
        self.assertEqual(10, tracks[9].track_number)
        self.assertEqual(15, tracks[9].track_total)
        self.assertEqual(11, tracks[10].track_number)
        self.assertEqual(15, tracks[10].track_total)
        self.assertEqual(12, tracks[11].track_number)
        self.assertEqual(15, tracks[11].track_total)
        self.assertEqual(13, tracks[12].track_number)
        self.assertEqual(15, tracks[12].track_total)
        self.assertEqual(14, tracks[13].track_number)
        self.assertEqual(15, tracks[13].track_total)
        self.assertEqual(15, tracks[14].track_number)
        self.assertEqual(15, tracks[14].track_total)

    def test__from_discogs_release__release_has_artists_on_tracks__the_tracks_should_have_artists_assigned(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(1451817)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release_model.get_tracks()
        self.assertEqual('Various', release_model.artist)
        self.assertEqual('Legowelt', tracks[0].artist)
        self.assertEqual('Bangkok Impact', tracks[1].artist)
        self.assertEqual('Orgue Electronique', tracks[2].artist)
        self.assertEqual('Schmerzlabor', tracks[3].artist)
        self.assertEqual('Bangkok Impact', tracks[4].artist)
        self.assertEqual('Orgue Electronique', tracks[5].artist)
        self.assertEqual('Legowelt', tracks[6].artist)
        self.assertEqual('Mr. Clavio', tracks[7].artist)
        self.assertEqual('Kassen', tracks[8].artist)

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

    def test__from_discogs_release__release_has_a_duplicate_artist__the_number_should_be_stripped_from_the_artist(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(155509)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual('Dr. Rhythm', release_model.artist)

    def test__from_discogs_release__release_has_a_duplicate_artists__the_number_should_be_stripped_from_the_artists(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(5459202)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(u'Noize Choir, Wax Magentic, Steve Legget, Shemale, Mike McHugh', release_model.artist)

    def test__from_discogs_release__release_has_duplicate_artists_on_tracks__the_number_should_be_stripped_from_the_artist(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(480352)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        tracks = release_model.get_tracks()
        self.assertEqual('Various', release_model.artist)
        self.assertEqual('Franck Sarrio', tracks[0].artist)
        self.assertEqual('Subliminal Criminal', tracks[1].artist)
        self.assertEqual('AU', tracks[2].artist)
        self.assertEqual('Duracel', tracks[3].artist)
        self.assertEqual('Nimoy', tracks[4].artist)
        self.assertEqual('Syncom Data', tracks[5].artist)
        self.assertEqual('Rude 66', tracks[6].artist)
        self.assertEqual('Hank', tracks[7].artist)

    def test__from_discogs_release__release_has_no_descriptions_in_format__the_format_should_be_parsed_correctly(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(34031)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual(release_model.format, 'CD')

    def test__from_discogs_release__release_has_artist_beginning_with_the__artist_should_be_changed_to_use_the_suffix(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(691856)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual('Beatles, The', release_model.artist)

    def test__from_discogs_release__release_has_multiple_artists_and_one_beginning_with_the__artist_should_be_changed_to_use_the_suffix(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(781647)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual('Murat & Advent, The', release_model.artist)

    def test__from_discogs_release__release_has_multiple_the_artists__artist_should_be_changed_to_use_the_suffix(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(105438)
        discogs_release.refresh()
        release_model = ReleaseModel.from_discogs_release(discogs_release)
        self.assertEqual('Bug, The Vs Rootsman, The Featuring He-Man', release_model.artist)

    def test__from_discogs_release__track_has_artist_beginning_with_the__artist_should_be_changed_to_use_the_suffix(self):
        client = discogs_client.Client('amu/0.1')
        discogs_release = client.release(339157)
        discogs_release.refresh()
        track_model = ReleaseModel.from_discogs_release(discogs_release).get_tracks()[5]
        self.assertEqual('Other People Place, The', track_model.artist)
