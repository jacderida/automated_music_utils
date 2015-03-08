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
        self._year = 0
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
        release_model.artist = ReleaseModel._get_artists_from_discogs_model(release)
        release_model.title = release.title
        release_model.label = release.labels[0].name
        release_model.catno = release.data['labels'][0]['catno']
        release_model.format = ReleaseModel._get_format_from_discogs_model(release.formats)
        release_model.year = release.master.main_release.year
        release_model.country = release.country
        release_model.genre = release.genres[0]
        ReleaseModel._get_tracks_from_discogs_model(release_model, release.tracklist)
        return release_model

    @staticmethod
    def _get_artists_from_discogs_model(release):
        artists = release.data["artists"]
        artists_string = ''
        for artist in artists:
            if artist["anv"]:
                artists_string += artist["anv"]
            else:
                artists_string += artist["name"]
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
    def _get_tracks_from_discogs_model(release_model, tracklist):
        for i, track in enumerate(tracklist):
            track_model = TrackModel()
            track_model.position = i + 1
            track_model.title = track.title
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
