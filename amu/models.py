import re

class TrackModel(object):
    def __init__(self):
        self._artist = ''
        self._title = ''
        self._track_number = 0
        self._track_total = 0
        self._disc_number = 0
        self._disc_total = 0

    @staticmethod
    def from_discogs_track(track, track_number, track_total, disc_number, disc_total):
        """ Converts a discogs track to a track in our domain.

        :track: The discogs track.
        because the discogs position will be things like "A1" for
        vinyl releases.
        :returns: The track model in our application domain.

        """
        track_model = TrackModel()
        track_model.track_number = track_number
        track_model.track_total = track_total
        track_model.disc_number = disc_number
        track_model.disc_total = disc_total
        track_model.title = track.title
        if "artists" in track.data:
            track_model.artist = ArtistHelper.get_artists(track.data["artists"])
        return track_model

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def track_number(self):
        return self._track_number

    @track_number.setter
    def track_number(self, value):
        self._track_number = value

    @property
    def track_total(self):
        return self._track_total

    @track_total.setter
    def track_total(self, value):
        self._track_total = value

    @property
    def disc_number(self):
        return self._disc_number

    @disc_number.setter
    def disc_number(self, value):
        self._disc_number = value

    @property
    def disc_total(self):
        return self._disc_total

    @disc_total.setter
    def disc_total(self, value):
        self._disc_total = value

class ReleaseModel(object):
    def __init__(self):
        self._discogs_id = 0
        self._artist = ''
        self._label = ''
        self._catno = ''
        self._title = ''
        self._format = ''
        self._format_quantity = 0
        self._country = ''
        self._year = ''
        self._original_year = ''
        self._genre = ''
        self._style = ''
        self._tracks = []

    def __repr__(self):
        return """ID: {0}
        Artist: {1}
        Title: {2}
        Label: {3}
        Cat No: {4}
        Format: {5}
        Country: {6}
        Released: {7}
        Originally Released: {8}
        Genre: {9}
        """.format(
            self.discogs_id, self.artist, self.title, self.label,
            self.catno, self.format, self.country, self.year, self.original_year,
            self.genre)

    @staticmethod
    def from_discogs_release(release):
        """ Converts a release from a discogs model to a simpler model
        in our domain.

        :release: The discogs based release model.
        :returns: The simpler model from our application domain.

        """
        release_model = ReleaseModel()
        release_model.discogs_id = release.id
        release_model.artist = ArtistHelper.get_artists(release.data["artists"])
        release_model.title = release.title
        release_model.label = ReleaseModel._get_labels_from_discogs_model(release.labels)
        release_model.catno = ReleaseModel._get_cat_numbers_from_discogs_model(release)
        release_model.format = ReleaseModel._get_format_from_discogs_model(release.formats)
        release_model.format_quantity = ReleaseModel._get_format_quantity_from_discogs_model(release.formats)
        release_model.country = release.country
        release_model.genre = ReleaseModel._get_genre_from_discogs_model(release.genres)
        ReleaseModel._get_date_from_discogs_model(release_model, release)
        ReleaseModel._get_tracks_from_discogs_model(release_model, release.tracklist)
        return release_model

    @staticmethod
    def _get_date_from_discogs_model(release_model, release):
        release_model.year = 'Unknown'
        if release.year != 0:
            release_model.year = str(release.year)
            release_model.original_year = str(release.year)
        if release.master != None:
            release_model.original_year = str(release.master.main_release.year)

    @staticmethod
    def get_artists_from_discogs_model(artist_data):
        artists_string = ''
        for artist in artist_data:
            if artist["anv"]:
                artists_string += artist["anv"]
            else:
                artists_string += artist["name"]
            join = artist["join"]
            if join:
                if join == ",":
                    artists_string += "{0} ".format(join)
                else:
                    artists_string += " {0} ".format(join)
        return artists_string

    @staticmethod
    def _get_format_from_discogs_model(formats):
        discogs_format = formats[0]
        format_string = "{0}, ".format(discogs_format["name"])
        descriptions = discogs_format["descriptions"]
        for i, description in enumerate(descriptions):
            format_string += description
            if i < len(descriptions) - 1:
                format_string += ", "
        return format_string

    @staticmethod
    def _get_format_quantity_from_discogs_model(formats):
        discogs_format = formats[0]
        return int(discogs_format["qty"])

    @staticmethod
    def _get_genre_from_discogs_model(genres):
        if len(genres) == 1:
            return genres[0]
        genre_string = ''
        for i, genre in enumerate(genres):
            genre_string += genre
            if i < len(genres) - 1:
                genre_string += ", "
        return genre_string

    @staticmethod
    def _get_labels_from_discogs_model(labels):
        if len(labels) == 1:
            return labels[0].name
        label_string = ''
        for i, label in enumerate(labels):
            label_string += label.name
            if i < len(labels) - 1:
                label_string += ', '
        return label_string

    @staticmethod
    def _get_cat_numbers_from_discogs_model(release):
        labels = release.data['labels']
        if len(labels) == 1:
            return labels[0]['catno']
        catno_string = ''
        for i, label in enumerate(labels):
            catno_string += label['catno']
            if i < len(labels) - 1:
                catno_string += ', '
        return catno_string

    @staticmethod
    def _get_tracks_from_discogs_model(release_model, tracklist):
        track_data = ReleaseModel._get_track_data(release_model, tracklist)
        i = 0
        for track in tracklist:
            if track.position:
                track_model = TrackModel.from_discogs_track(
                    track, track_data[i][0], track_data[i][1], track_data[i][2], track_data[i][3])
                i += 1
                release_model.add_track(track_model)

    @staticmethod
    def _get_track_data(release_model, tracklist):
        if 'CD' in release_model.format:
            if release_model.format_quantity == 1:
                return ReleaseModel._get_single_disc_track_data(tracklist)
            return ReleaseModel._get_multi_disc_track_data(release_model.format_quantity, tracklist)
        return ReleaseModel._get_single_disc_track_data(tracklist)

    @staticmethod
    def _get_single_disc_track_data(tracklist):
        track_totals = []
        track_number = 1
        track_total = len([x for x in tracklist if x.position])
        for track in tracklist:
            if track.position: # Track with no position is an index track.
                track_totals.append((track_number, track_total, 1, 1))
                track_number += 1
        return track_totals

    @staticmethod
    def _get_multi_disc_track_data(disc_total, tracklist):
        track_totals_per_disc = ReleaseModel._get_track_totals_per_disc(tracklist)
        i = 0
        track_data = []
        track_number = 1
        track_total = track_totals_per_disc[i]
        disc_number = 1
        for track in tracklist:
            if track.position: # Track with no position is an index track.
                track_data.append((track_number, track_total, disc_number, disc_total))
                if track_number == track_total:
                    i += 1
                    if i >= len(track_totals_per_disc): # We are on the last track - bail out.
                        break
                    disc_number += 1
                    track_total = track_totals_per_disc[i]
                    track_number = 1
                else:
                    track_number += 1
        return track_data

    @staticmethod
    def _get_track_totals_per_disc(tracklist):
        track_totals_per_disc = []
        track_total = 1
        disc_number = 1
        for track in tracklist:
            if track.position:
                if '-' in track.position:
                    discogs_disc_number = int(track.position.split('-')[0])
                    if discogs_disc_number != disc_number:
                        disc_number += 1
                        track_totals_per_disc.append(track_total - 1)
                        track_total = 1
                    track_total += 1
        track_totals_per_disc.append(track_total - 1)
        return track_totals_per_disc

    @property
    def discogs_id(self):
        return self._discogs_id

    @discogs_id.setter
    def discogs_id(self, value):
        self._discogs_id = value

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value

    @property
    def catno(self):
        return self._catno

    @catno.setter
    def catno(self, value):
        self._catno = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value

    @property
    def format_quantity(self):
        return self._format_quantity

    @format_quantity.setter
    def format_quantity(self, value):
        self._format_quantity = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        self._country = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def original_year(self):
        return self._original_year

    @original_year.setter
    def original_year(self, value):
        self._original_year = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        self._style = value

    def add_track(self, track):
        """Adds a track to the collection

        :track: The track to be added to the release.

        """
        if track == None:
            raise ValueError('A non-null value must be supplied for the track')
        if type(track) != TrackModel:
            raise ValueError('The track must be a TrackModel object')
        self._tracks.append(track)

    def add_track_directly(self, artist, title, track_number, track_total, disc_number, disc_total):
        """ Horrible method to be used in testing code. """
        track = TrackModel()
        track.artist = artist
        track.title = title
        track.track_number = track_number
        track.track_total = track_total
        track.disc_number = disc_number
        track.disc_total = disc_total
        self._tracks.append(track)

    def get_tracks(self):
        """ Gets the tracks as a tuple.
        :returns: The tracks as a read only list.
        """
        return tuple(self._tracks)

class ArtistHelper(object):
    @staticmethod
    def get_artists(artist_data):
        artists_string = ''
        for artist in artist_data:
            if artist["anv"]:
                artists_string += artist["anv"]
            else:
                artists_string += artist["name"]
            artists_string = ArtistHelper._remove_number_from_duplicate_artist(artists_string)
            join = artist["join"]
            if join:
                if join == ",":
                    artists_string += "{0} ".format(join)
                else:
                    artists_string += " {0} ".format(join)
        stripped_artists = artists_string.strip()
        if stripped_artists[-1] == ',':
            """
            For some utterly bizarre reason, on releases like compilations that have
            artists on tracks, even if there's only one artist, there's still a join
            present, in the form of a comma. This little piece of code returns the artist
            less the superfluous comma at the end.
            """
            return stripped_artists[0:-1]
        return artists_string

    @staticmethod
    def _remove_number_from_duplicate_artist(artist):
        """
        Discogs deals with duplicate artists by appending a number to the artist.
        For example, if there are 2 artists named 'Aphex Twin', there will be an
        entry for Aphex Twin and Aphex Twin (2).

        This code detects that and then strips it off.
        """
        match = re.search('.*(\(\d+\))', artist)
        if match:
            artist = artist[0:match.start(1)].strip()
        return artist

