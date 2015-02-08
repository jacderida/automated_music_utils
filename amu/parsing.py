import os
from amu.commands.ripcdcommand import RipCdCommand
from amu.commands.encodewavtomp3command import EncodeWavToMp3Command

class CommandParser(object):
    """ Responsible for parsing the string based command from the command line
        into a command object that can be executed.
    """
    def __init__(self, configuration_provider, cd_ripper, encoder):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._encoder = encoder

    def from_args(self, args):
        if args.command == 'rip':
            return self._get_rip_command(args)
        elif args.command == 'encode':
            return self._get_encode_command(args)

    def _get_rip_command(self, args):
        command = RipCdCommand(self._configuration_provider, self._cd_ripper)
        if args.destination:
            command.destination = args.destination
        else:
            command.destination = os.getcwd()
        return command

    def _get_encode_command(self, args):
        if args.encoding_from == 'wav' and args.encoding_to == 'mp3':
            command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
            if args.source:
                command.source = args.source
            else:
                command.source = os.getcwd()
            if args.destination:
                command.destination = args.destination
            else:
                command.destination = os.getcwd()
            if args.keep_source:
                command.keep_source = True
            return command

class EncodeCommandParser(object):
    def __init__(self, configuration_provider, cd_ripper, encoder):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._encoder = encoder

    def parse_wav_to_mp3(self, source, destination):
        if not os.path.exists(source):
            raise CommandParsingError('The source directory or wav file must exist')
        some_string = 'ddd'
        if os.path.isfile(source):
            command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
            command.source = source
            command.destination = destination
            return command
        commands = []
        for root, directories, files in os.walk(source):
            for source_wav in [f for f in files if f.endswith(".wav")]:
                multi_cd_directory = ''
                if root != source:
                    multi_cd_directory = os.path.basename(root)
                command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
                command.source = os.path.join(source, multi_cd_directory, source_wav)
                command.destination = os.path.join(destination, multi_cd_directory, os.path.splitext(source_wav)[0] + ".mp3")
                commands.append(command)
        return commands


class CommandParsingError(Exception):
    def __init__(self, message):
        super(CommandParsingError, self).__init__(message)
        self.message = message
