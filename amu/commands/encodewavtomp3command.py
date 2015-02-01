from amu.commands.command import Command
from amu.commands.command import CommandValidationError
from amu.encode import LameEncoder

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
        if not self.source:
            raise CommandValidationError('A source must be specified for encoding a wav to mp3')

    def execute(self):
        self._encoder.encode_wav_to_mp3(self.source, self.destination)
