import os
from tagger import ID3v2
from tagger.constants import ID3V2_FIELD_ENC_UTF16
from amu.encode import LameEncoder
from amu.rip import RubyRipperCdRipper

class CommandValidationError(Exception):
    def __init__(self, message):
        super(CommandValidationError, self).__init__(message)
        self.message = message

class Command(object):
    """ Base command that provides functionality common to all commands. """
    def __init__(self, config_provider):
        self._config_provider = config_provider

    def validate(self):
        """ Validates the command before execution. """
        pass

    def execute(self):
        """ Executes the command. """
        pass

class EncodeWavToMp3Command(Command):
    def __init__(self, config_provider, encoder):
        super(EncodeWavToMp3Command, self).__init__(config_provider)
        if encoder is None:
            encoder = LameEncoder(config_provider)
        self._encoder = encoder
        self._source = ''
        self._destination = ''
        self._keep_source = False

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def keep_source(self):
        return self._keep_source

    @keep_source.setter
    def keep_source(self, value):
        self._keep_source = value

    def validate(self):
        if self.source:
            if not os.path.exists(self.source):
                raise CommandValidationError('The specified source does not exist.')
            if os.path.isdir(self.source):
                raise CommandValidationError('The source cannot be a directory.')
        else:
            raise CommandValidationError('A source must be specified for encoding a wav to mp3')
        if not self.destination:
            raise CommandValidationError('A destination must be specified for encoding a wav to mp3')

    def execute(self):
        directory_path = os.path.dirname(self.destination)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        self._encoder.encode_wav_to_mp3(self.source, self.destination)
        if not self.keep_source:
            os.remove(self.source)

class RipCdCommand(Command):
    def __init__(self, config_provider, cd_ripper):
        super(RipCdCommand, self).__init__(config_provider)
        if cd_ripper is None:
            cd_ripper = RubyRipperCdRipper(config_provider)
        self._cd_ripper = cd_ripper
        self._destination = ''

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    def validate(self):
        if not self.destination:
            raise CommandValidationError('A destination must be supplied for the CD rip')

    def execute(self):
        self._cd_ripper.rip_cd(self.destination)

class AddMp3TagCommand(Command):
    def __init__(self, config_provider):
        super(AddMp3TagCommand, self).__init__(config_provider)
        self._source = ''
        self._artist = ''
        self._title = ''
        self._album = ''
        self._year = ''
        self._genre = ''
        self._track_number = 0
        self._track_total = 0

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

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
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

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
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    def validate(self):
        if not os.path.exists(self._source):
            raise CommandValidationError('The specified mp3 source does not exist.')
        if os.path.isdir(self._source):
            raise CommandValidationError('The source must be an mp3, not a directory.')
        if not self._artist:
            raise CommandValidationError('An artist must be supplied for the tag.')
        if not self._album:
            raise CommandValidationError('An album must be supplied for the tag.')
        if not self._title:
            raise CommandValidationError('A title must be supplied for the tag.')
        if self._track_number < 1:
            raise CommandValidationError('The track number must be at least 1.')
        if self._track_number > self._track_total:
            raise CommandValidationError('The track number cannot be greater than the track total.')

    def execute(self):
        tag = ID3v2(self._source)
        self._add_artist_frame(tag)
        self._add_title_frame(tag)
        self._add_album_frame(tag)
        self._add_year_frame(tag)
        self._add_track_number_frame(tag)
        self._add_genre_frame(tag)
        tag.commit()

    def _add_artist_frame(self, tag):
        artist_frame = tag.new_frame("TPE1")
        artist_frame.set_text(self._artist)
        tag.frames.append(artist_frame)

    def _add_title_frame(self, tag):
        title_frame = tag.new_frame("TIT2")
        title_frame.set_text(self._title)
        tag.frames.append(title_frame)

    def _add_album_frame(self, tag):
        album_frame = tag.new_frame("TALB")
        album_frame.set_text(self._album)
        tag.frames.append(album_frame)

    def _add_year_frame(self, tag):
        if self._year:
            year_frame = tag.new_frame("TYER")
            year_frame.set_text(self._year)
            tag.frames.append(year_frame)

    def _add_track_number_frame(self, tag):
        track_number_frame = tag.new_frame("TRCK")
        track_number_string = str(self._track_number)
        track_total_string = str(self._track_total)
        if self._track_number < 10:
            track_number_string = "0{0}".format(self._track_number)
        if self._track_total < 10:
            track_total_string = "0{0}".format(self._track_total)
        track_number_frame.set_text("{0}/{1}".format(track_number_string, track_total_string))
        tag.frames.append(track_number_frame)

    def _add_genre_frame(self, tag):
        if self._genre:
            genre_frame = tag.new_frame("TCON")
            genre_frame.set_text(self._genre)
            tag.frames.append(genre_frame)
