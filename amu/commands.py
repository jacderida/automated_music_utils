import os
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