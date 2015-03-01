class TrackModel(object):
    def __init__(self):
        self._artist = ''
        self._title = ''
        self._position = 0

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
        self._genre = ''
        self._style = ''
        self._tracks = []

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
