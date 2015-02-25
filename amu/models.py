class Track(object):
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
