class TrackModel(object):
    def __init__(self):
        self._artist = ''
        self._title = ''
        self._position = 0

    @staticmethod
    def from_discogs_track(track, position):
        """ Converts a discogs track to a track in our domain.

        :track: The discogs track.
        :position: The position of the track. This needs to come from outside,
        because the discogs position will be things like "A1" for
        vinyl releases.
        :returns: The track model in our application domain.

        """
        track_model = TrackModel()
        track_model.position = position
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
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

class ReleaseModel(object):
    def __init__(self):
        self._artist = ''
        self._label = ''
        self._catno = ''
        self._title = ''
        self._format = ''
        self._country = ''
        self._year = ''
        self._genre = ''
        self._style = ''
        self._tracks = []

    @staticmethod
    def from_discogs_release(release):
        """ Converts a release from a discogs model to a simpler model
        in our domain.

        :release: The discogs based release model.
        :returns: The simpler model from our application domain.

        """
        release_model = ReleaseModel()
        release_model.artist = ArtistHelper.get_artists(release.data["artists"])
        release_model.title = release.title
        release_model.label = ReleaseModel._get_labels_from_discogs_model(release.labels)
        release_model.year = ReleaseModel._get_date_from_discogs_model(release)
        release_model.catno = ReleaseModel._get_cat_numbers_from_discogs_model(release)
        release_model.format = ReleaseModel._get_format_from_discogs_model(release.formats)
        release_model.country = release.country
        release_model.genre = ReleaseModel._get_genre_from_discogs_model(release.genres)
        ReleaseModel._get_tracks_from_discogs_model(release_model, release.tracklist)
        return release_model

    @staticmethod
    def _get_date_from_discogs_model(release):
        date = 'Unknown'
        if release.master != None:
            date = str(release.master.main_release.year)
        elif release.year != 0:
            date = str(release.year)
        return date

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
        for i, track in enumerate(tracklist):
            if track.position: # If track has no position, it's an index track.
                track_model = TrackModel.from_discogs_track(track, i + 1)
                release_model.add_track(track_model)

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
            join = artist["join"]
            if join:
                if join == ",":
                    artists_string += "{0} ".format(join)
                else:
                    artists_string += " {0} ".format(join)
        return artists_string
