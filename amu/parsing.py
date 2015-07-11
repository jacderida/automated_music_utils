import os
import tempfile
import uuid
from amu import utils
from amu.commands import RipCdCommand
from amu.commands import EncodeWavToMp3Command
from amu.commands import TagMp3Command


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
        elif args.command == 'tag':
            return self._get_tag_command(args)

    def _get_rip_command(self, args):
        command = RipCdCommand(self._configuration_provider, self._cd_ripper)
        if args.destination:
            command.destination = args.destination
        else:
            command.destination = os.getcwd()
        return [command]

    def _get_encode_command(self, args):
        if args.destination:
            destination = args.destination
        else:
            destination = os.getcwd()
        encode_command_parser = EncodeCommandParser(
            self._configuration_provider, self._cd_ripper, self._encoder)
        if args.encoding_from == 'cd' and args.encoding_to == 'mp3':
            commands = encode_command_parser.parse_cd_rip(
                os.path.join(tempfile.gettempdir(), str(uuid.uuid4())),
                destination,
                utils.get_number_of_tracks_on_cd())
        if args.encoding_from == 'wav' and args.encoding_to == 'mp3':
            if args.source:
                source = args.source
            else:
                source = os.getcwd()
            commands = encode_command_parser.parse_wav_to_mp3(source, destination)
            if len(commands) == 0:
                raise CommandParsingError('The source directory has no wavs to encode')
        if args.keep_source:
            for command in commands:
                command.keep_source = True
        return commands

    def _get_tag_command(self, args):
        command = TagMp3Command(self._configuration_provider)
        return [command]

class EncodeCommandParser(object):
    def __init__(self, configuration_provider, cd_ripper, encoder):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._encoder = encoder

    def parse_cd_rip(self, rip_destination, destination, track_count):
        if not rip_destination:
            raise CommandParsingError('The rip destination cannot be empty')
        if not destination:
            raise CommandParsingError('The destination cannot be empty')
        if track_count < 1:
            raise CommandParsingError('The track count must be greather than or equal to 1')
        commands = []
        rip_cd_command = RipCdCommand(self._configuration_provider, self._cd_ripper)
        rip_cd_command.destination = rip_destination
        commands.append(rip_cd_command)
        for i in range(1, track_count + 1):
            encode_wav_to_mp3_command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
            encode_wav_to_mp3_command.source = os.path.join(rip_destination, self._get_track_name(i, "wav"))
            encode_wav_to_mp3_command.destination = os.path.join(destination, self._get_track_name(i, "mp3"))
            commands.append(encode_wav_to_mp3_command)
        return commands

    def parse_wav_to_mp3(self, source, destination):
        if not os.path.exists(source):
            raise CommandParsingError('The source directory or wav file must exist')
        if not destination:
            raise CommandParsingError('The destination cannot be empty')
        if os.path.isfile(source):
            return self._get_single_file_command(source, destination)
        return self._get_directory_command(source, destination)

    def _get_track_name(self, track_number, extension):
        if track_number < 10:
            return "0{0} - Track {0}.{1}".format(track_number, extension)
        return "{0} - Track {0}.{1}".format(track_number, extension)

    def _get_single_file_command(self, source, destination):
        if not destination.endswith('.mp3'):
            raise CommandParsingError('If the source is a file, the destination must also be a file.')
        command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
        command.source = source
        command.destination = destination
        return [command]

    def _get_directory_command(self, source, destination):
        commands = []
        for root, directories, files in os.walk(source):
            for source_wav in [f for f in files if f.endswith(".wav")]:
                multi_cd_directory = ''
                if root != source:
                    multi_cd_directory = os.path.basename(root)
                command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
                command.source = os.path.join(source, multi_cd_directory, source_wav)
                command.destination = os.path.join(
                    destination, multi_cd_directory, os.path.splitext(source_wav)[0] + ".mp3")
                commands.append(command)
        return commands

class CommandParsingError(Exception):
    def __init__(self, message):
        super(CommandParsingError, self).__init__(message)
        self.message = message
