import os
from mutagen import File
from mutagen.id3 import COMM, ID3, ID3NoHeaderError, TALB, TCON, TDRC, TIT2, TPE1, TPOS, TRCK
from amu.audio import LameEncoder, RubyRipperCdRipper

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

class EncodeWavCommand(Command):
    def __init__(self, config_provider, encoder):
        super(EncodeWavCommand, self).__init__(config_provider)
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
            raise CommandValidationError('A source must be specified for encoding a wav')
        if not self.destination:
            raise CommandValidationError('A destination must be specified for encoding a wav')

    def execute(self):
        directory_path = os.path.dirname(self.destination)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        self._encoder.encode(self.source, self.destination)
        if not self.keep_source:
            os.remove(self.source)

class DecodeAudioCommand(Command):
    def __init__(self, config_provider, encoder):
        super(DecodeAudioCommand, self).__init__(config_provider)
        if encoder is None:
            encoder = LameEncoder(config_provider)
        self._encoder = encoder
        self._source = ''
        self._destination = ''

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

    def validate(self):
        if not self.source:
            raise ValueError('A source must be specified for decoding an audio file')

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

class AddTagCommand(Command):
    def __init__(self, config_provider, tagger):
        super(AddTagCommand, self).__init__(config_provider)
        self._source = ''
        self._artist = ''
        self._album_artist = ''
        self._title = ''
        self._album = ''
        self._year = ''
        self._genre = ''
        self._comment = ''
        self._track_number = 0
        self._track_total = 0
        self._disc_number = 0
        self._disc_total = 0
        self._tagger = tagger

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
    def album_artist(self):
        return self._album_artist

    @album_artist.setter
    def album_artist(self, value):
        self._album_artist = value

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

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value

    def validate(self):
        if not os.path.exists(self._source):
            raise CommandValidationError('The specified mp3 source does not exist.')
        if os.path.isdir(self._source):
            raise CommandValidationError('The source must be an mp3, not a directory.')
        if self._track_number < 1:
            raise CommandValidationError('The track number must be at least 1.')
        if self._track_number > self._track_total:
            raise CommandValidationError('The track number cannot be greater than the track total.')

    def execute(self):
        self._tagger.add_tags(
            self.source, self.artist, self.album_artist, self.album,
            self.title, self.year, self.genre, self.comment,
            self.track_number, self.track_total, self.disc_number, self.disc_total)

class RemoveTagCommand(Command):
    def __init__(self, config_provider, tagger):
        super(RemoveTagCommand, self).__init__(config_provider)
        self._tagger = tagger
        self._source = ''

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    def validate(self):
        if not self._source:
            raise ValueError('A source must be specified for the remove tag command.')
        if not os.path.exists(self._source):
            raise CommandValidationError('The specified source does not exist.')

    def execute(self):
        print "[tag] Removing tags from {0}".format(self.source)
        self._tagger.remove_tags(self.source)

class MoveAudioFileCommand(Command):
    def __init__(self, config_provider):
        super(MoveAudioFileCommand, self).__init__(config_provider)
        self._source = ''
        self._destination = ''

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

    def validate(self):
        if not self._source:
            raise CommandValidationError('A source must be supplied for the move audio file command.')
        if not os.path.exists(self._source):
            raise CommandValidationError('The source for the move audio file command must exist.')
        if os.path.isdir(self._source):
            raise CommandValidationError('The source for the move audio file command cannot be a directory.')
        if not self._destination:
            raise CommandValidationError('A destination must be supplied for the move audio file command.')
        source_extension = os.path.splitext(self._source)[1][1:]
        destination_extension = os.path.splitext(self._destination)[1][1:]
        if source_extension != destination_extension:
            raise CommandValidationError(
                'The move audio file command must operate on files of the same type. Source is {0} and destination is {1}.'.format(
                    source_extension, destination_extension))

    def execute(self):
        print u'[move] Moving file {0} to {1}'.format(self.source, self.destination)
        directory = os.path.dirname(self._destination)
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.rename(self.source, self.destination)

class FetchReleaseCommand(Command):
    def __init__(self, config_provider, metadata_service):
        super(FetchReleaseCommand, self).__init__(config_provider)
        self._metadata_service = metadata_service
        self._discogs_id = 0

    @property
    def discogs_id(self):
        return self._discogs_id

    @discogs_id.setter
    def discogs_id(self, value):
        self._discogs_id = value

    def validate(self):
        try:
            int(self.discogs_id)
        except ValueError:
            raise CommandValidationError('The fetch command must use a valid integer for the discogs ID.')

    def execute(self):
        release_model = self._metadata_service.get_release_by_id(self.discogs_id)
        print release_model

class AddArtworkCommand(Command):
    def __init__(self, config_provider, tagger):
        super(AddArtworkCommand, self).__init__(config_provider)
        self._tagger = tagger
        self._source = ''
        self._destination = ''

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

    def validate(self):
        if not self.source:
            raise CommandValidationError('A source must be supplied for the add artwork command.')
        if not os.path.exists(self.source):
            raise CommandValidationError('A valid source must be supplied for the add artwork command.')
        if not self.destination:
            raise CommandValidationError('A destination must be supplied for the add artwork command.')
        if not os.path.exists(self.destination):
            raise CommandValidationError('A valid destination must be supplied for the add artwork command.')

    def execute(self):
        self._tagger.apply_artwork(self.source, self.destination)
