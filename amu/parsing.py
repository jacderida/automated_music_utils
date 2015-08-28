import os
import tempfile
import uuid
from amu import utils
from amu.commands import AddMp3TagCommand
from amu.commands import EncodeWavToMp3Command
from amu.commands import MoveAudioFileCommand
from amu.commands import RipCdCommand
from amu.metadata import MaskReplacer


class CommandParser(object):
    """ Responsible for parsing the string based command from the command line
        into a command object that can be executed.
    """
    def __init__(self, configuration_provider, cd_ripper, encoder, metadata_service):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._encoder = encoder
        self._metadata_service = metadata_service
        self._mask_replacer = MaskReplacer()

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
        release_model = None
        if args.destination:
            destination = args.destination
        else:
            destination = os.getcwd()
        if args.discogs_id:
            release_model = self._metadata_service.get_release_by_id(int(args.discogs_id))
            if not args.destination:
                destination = self._configuration_provider.get_destination_with_mask_replaced(release_model)
        return self._get_encode_commands(args, destination, release_model)

    def _get_encode_commands(self, args, destination, release_model):
        if args.encoding_from == 'cd' and args.encoding_to == 'mp3':
            commands = self._get_encode_cd_to_mp3_commands(args, destination, release_model)
        elif args.encoding_from == 'wav' and args.encoding_to == 'mp3':
            commands = self._get_encode_wav_to_mp3_commands(args, destination, release_model)
        if args.keep_source:
            for command in commands:
                command.keep_source = True
        return commands

    def _get_tag_command(self, args):
        command_args = AddTagCommandArgs.from_args(args)
        if not command_args.source:
            command_args.source = os.getcwd()
        tag_command_parser = TagCommandParser(self._configuration_provider)
        commands = tag_command_parser.parse_add_mp3_tag_command(command_args)
        return commands

    def _get_encode_cd_to_mp3_commands(self, args, destination, release_model):
        commands = []
        encode_command_parser = EncodeCommandParser(self._configuration_provider, self._cd_ripper, self._encoder)
        track_count = utils.get_number_of_tracks_on_cd()
        source = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        encode_commands = encode_command_parser.parse_cd_rip(source, destination, track_count)
        commands.extend(encode_commands)
        if release_model:
            # The first command is a rip cd command, which we don't need.
            commands.extend(self._get_release_tag_commands(args, encode_commands[1:], destination, release_model))
            move_file_parser = MoveAudioFileCommandParser(self._configuration_provider)
            commands.extend(move_file_parser.parse_from_encode_commands(encode_commands[1:], release_model))
        return commands

    def _get_encode_wav_to_mp3_commands(self, args, destination, release_model):
        if args.source:
            source = args.source
        else:
            source = os.getcwd()
        commands = []
        encode_command_parser = EncodeCommandParser(self._configuration_provider, self._cd_ripper, self._encoder)
        encode_commands = encode_command_parser.parse_wav_to_mp3(source, destination)
        commands.extend(encode_commands)
        track_count = len(encode_commands)
        if track_count == 0:
            raise CommandParsingError('The source directory has no wavs to encode')
        if release_model:
            commands.extend(self._get_release_tag_commands(args, encode_commands, destination, release_model))
            move_file_parser = MoveAudioFileCommandParser(self._configuration_provider)
            commands.extend(move_file_parser.parse_from_encode_commands(encode_commands, release_model))
        return commands

    def _get_release_tag_commands(self, args, commands, destination, release_model):
        release_track_count = len(release_model.get_tracks())
        track_count = len(commands)
        if track_count != release_track_count:
            raise CommandParsingError(
                'The source has {0} tracks and the discogs release has {1}. The number of tracks on both must be the same.'.format(track_count, release_track_count))
        tag_command_parser = TagCommandParser(self._configuration_provider)
        if args.encoding_from == 'cd':
            return tag_command_parser.parse_from_release_model_with_empty_source(destination, release_model)
        return tag_command_parser.parse_from_release_model_with_sources(
            release_model, [x.destination for x in commands])

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
            command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
            command.source = os.path.join(rip_destination, utils.get_track_name(i, "wav"))
            command.destination = os.path.join(destination, utils.get_track_name(i, "mp3"))
            commands.append(command)
        return commands

    def parse_wav_to_mp3(self, source, destination):
        if not os.path.exists(source):
            raise CommandParsingError('The source directory or wav file must exist')
        if not destination:
            raise CommandParsingError('The destination cannot be empty')
        if os.path.isfile(source):
            return self._get_single_file_command(source, destination)
        return self._get_directory_command(source, destination)

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
            if len(directories) > 0:
                for directory in sorted(directories):
                    full_source_directory = os.path.join(root, directory)
                    full_destination_directory = os.path.join(destination, directory)
                    for source_wav in [f for f in sorted(os.listdir(full_source_directory)) if f.endswith('.wav')]:
                        commands.append(self._get_encode_wav_to_mp3_command(
                            full_source_directory, full_destination_directory, source_wav))
            else:
                for source_wav in [f for f in sorted(files) if f.endswith('.wav')]:
                    commands.append(self._get_encode_wav_to_mp3_command(
                        root, destination, source_wav))
            break
        return commands

    def _get_encode_wav_to_mp3_command(self, source_directory, destination_directory, source_wav):
        command = EncodeWavToMp3Command(self._configuration_provider, self._encoder)
        command.source = os.path.join(source_directory, source_wav)
        command.destination = os.path.join(destination_directory, os.path.splitext(source_wav)[0] + '.mp3')
        return command

class TagCommandParser(object):
    def __init__(self, configuration_provider):
        self._configuration_provider = configuration_provider

    def parse_from_release_model_with_sources(self, release_model, sources):
        commands = []
        tracks = release_model.get_tracks()
        if len(tracks) != len(sources):
            raise CommandParsingError('The source must have the same number of tracks as the release.')
        for i, source in enumerate(sources):
            commands.append(self._get_add_tag_command_from_release_model(source, release_model, tracks[i]))
        return commands

    def parse_from_release_model_with_empty_source(self, source_path, release_model):
        """ Gets a set of add tag commands based on the tracks on the release model.
        The source for the commands will be assumed file names, based on the amount of tracks on
        the release model.

        This is going to be used for encoding CDs. It's not enough to point toward
        the directory where the CD is going to be ripped to, and then use the
        parse_from_release_model method, because the parsing occurs before the CD is ripped,
        and so the track files don't yet exist. That method relies on there being pre-existing
        files to use for the source for the command.

        :source_path: The path where the MP3s will eventually be.
        :release_model: The release model with the metadata for the tags.
        :returns: A list of add tag commands.

        """
        commands = []
        track_number = 1
        for track in release_model.get_tracks():
            full_source_path = os.path.join(source_path, utils.get_track_name(track_number, "mp3"))
            commands.append(self._get_add_tag_command_from_release_model(full_source_path, release_model, track))
            track_number += 1
        return commands

    def parse_from_release_model(self, source_path, release_model):
        i = 0
        commands = []
        tracks = release_model.get_tracks()
        for root, directories, files in os.walk(source_path):
            if len(directories) > 0:
                for directory in sorted(directories):
                    full_source_directory = os.path.join(root, directory)
                    for source_file in [f for f in sorted(os.listdir(full_source_directory)) if f.endswith(".mp3")]:
                        full_source_path = os.path.join(full_source_directory, source_file)
                        command = self._get_add_tag_command_from_release_model(full_source_path, release_model, tracks[i])
                        commands.append(command)
                        i += 1
            else:
                for source_file in [f for f in sorted(files) if f.endswith(".mp3")]:
                    full_source = os.path.join(root, source_file)
                    command = self._get_add_tag_command_from_release_model(full_source, release_model, tracks[i])
                    commands.append(command)
                    i += 1
            break
        return commands

    def parse_add_mp3_tag_command(self, command_args):
        if os.path.isfile(command_args.source):
            return self._get_single_file_command(command_args)
        if command_args.track_total != 0:
            raise CommandParsingError('With a directory source, a track number and total override cannot be specified.')
        return self._get_directory_command(command_args)

    def _get_single_file_command(self, command_args):
        command = self._get_add_mp3_command(command_args.source, command_args)
        return [command]

    def _get_directory_command(self, command_args):
        commands = []
        for root, directories, files in os.walk(command_args.source):
            directory_len = len(directories)
            if directory_len > 0:
                disc_number = 1
                disc_total = directory_len
                for directory in sorted(directories):
                    full_source_directory = os.path.join(root, directory)
                    mp3_files = [f for f in sorted(os.listdir(full_source_directory)) if f.endswith(".mp3")]
                    track_total = len(mp3_files)
                    track_number = 1
                    for source_file in mp3_files:
                        full_source_path = os.path.join(full_source_directory, source_file)
                        command_args.disc_number = disc_number
                        command_args.disc_total = disc_total
                        command = self._get_add_mp3_command(full_source_path, command_args)
                        command.track_number = track_number
                        command.track_total = track_total
                        commands.append(command)
                        track_number += 1
                    disc_number += 1
            else:
                mp3_files = [f for f in sorted(files) if f.endswith(".mp3")]
                track_total = len(mp3_files)
                track_number = 1
                for source_file in mp3_files:
                    full_source_path = os.path.join(root, source_file)
                    command = self._get_add_mp3_command(full_source_path, command_args)
                    command.track_number = track_number
                    command.track_total = track_total
                    commands.append(command)
                    track_number += 1
            break
        return commands

    def _get_add_tag_command_from_release_model(self, source, release_model, track):
        command_args = AddTagCommandArgs()
        if track.artist:
            command_args.artist = track.artist
        else:
            command_args.artist = release_model.artist
        command_args.album = release_model.title
        command_args.title = track.title
        command_args.year = release_model.year
        command_args.genre = release_model.genre
        command_args.comment = '{0} ({1})'.format(release_model.label, release_model.catno)
        command_args.track_number = track.track_number
        command_args.track_total = track.track_total
        command_args.disc_number = track.disc_number
        command_args.disc_total = track.disc_total
        return self._get_add_mp3_command(source, command_args)

    def _get_add_mp3_command(self, source, command_args):
        command = AddMp3TagCommand(self._configuration_provider)
        command.source = source
        command.artist = command_args.artist
        command.album = command_args.album
        command.title = command_args.title
        command.year = command_args.year
        command.genre = command_args.genre
        command.comment = command_args.comment
        self._set_track_information(command, command_args)
        self._set_disc_information(command, command_args)
        return command

    def _set_track_information(self, command, command_args):
        if command_args.track_number == 0:
            command.track_number = 1
            command.track_total = 1
        else:
            if command_args.track_total == 0:
                raise CommandParsingError('If a track number has been supplied, a track total must also be supplied.')
            command.track_number = command_args.track_number
            command.track_total = command_args.track_total

    def _set_disc_information(self, command, command_args):
        if command_args.disc_number == 0:
            command.disc_number = 1
            command.disc_total = 1
        else:
            if command_args.disc_total == 0:
                raise CommandParsingError('If a disc number has been supplied, a disc total must also be supplied.')
            command.disc_number = command_args.disc_number
            command.disc_total = command_args.disc_total

class MoveAudioFileCommandParser(object):
    def __init__(self, configuration_provider):
        self._configuration_provider = configuration_provider

    def parse_from_encode_commands(self, encode_commands, release_model):
        i = 0
        commands = []
        tracks = release_model.get_tracks()
        if len(tracks) != len(encode_commands):
            raise CommandParsingError('The number of encode commands must be the same as the number of tracks on the release.')
        while i < len(encode_commands):
            command = MoveAudioFileCommand(self._configuration_provider)
            command.source = encode_commands[i].destination
            command.destination = self._get_destination(encode_commands[i].destination, tracks[i])
            commands.append(command)
            i += 1
        return commands

    def _get_destination(self, destination, track):
        directory_path = os.path.dirname(destination)
        extension = os.path.splitext(destination)[1][1:] # ignore the . that splitext returns
        track_number = ''
        if track.track_number < 10:
            track_number = '0' + str(track.track_number)
        else:
            track_number = track.track_number
        return u'{0}/{1} - {2}.{3}'.format(directory_path, track_number, track.title, extension)

class AddTagCommandArgs(object):
    def __init__(self):
        self._source = ''
        self._artist = ''
        self._title = ''
        self._album = ''
        self._year = ''
        self._genre = ''
        self._comment = ''
        self._track_number = 0
        self._track_total = 0
        self._disc_number = 0
        self._disc_total = 0

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

    @staticmethod
    def from_args(args):
        command_args = AddTagCommandArgs()
        command_args.source = AddTagCommandArgs._get_value_from_args(args.source)
        command_args.artist = AddTagCommandArgs._get_value_from_args(args.artist)
        command_args.album = AddTagCommandArgs._get_value_from_args(args.album)
        command_args.title = AddTagCommandArgs._get_value_from_args(args.title)
        command_args.genre = AddTagCommandArgs._get_value_from_args(args.genre)
        command_args.comment = AddTagCommandArgs._get_value_from_args(args.comment)
        command_args.year = AddTagCommandArgs._get_numeric_value_from_args(args.year)
        command_args.track_number = AddTagCommandArgs._get_numeric_value_from_args(args.track_number)
        command_args.track_total = AddTagCommandArgs._get_numeric_value_from_args(args.track_total)
        command_args.disc_number = AddTagCommandArgs._get_numeric_value_from_args(args.disc_number)
        command_args.disc_total = AddTagCommandArgs._get_numeric_value_from_args(args.disc_total)
        return command_args

    @staticmethod
    def _get_numeric_value_from_args(args_value):
        value = AddTagCommandArgs._get_value_from_args(args_value)
        if not value:
            return 0
        return int(value)

    @staticmethod
    def _get_value_from_args(args_value):
        if not args_value:
            return ''
        return AddTagCommandArgs._dequote(args_value)

    @staticmethod
    def _dequote(s):
        if (s[0] == s[-1]) and s.startswith(("'", '"')):
            return s[1:-1]
        return s

class CommandParsingError(Exception):
    def __init__(self, message):
        super(CommandParsingError, self).__init__(message)
        self.message = message
