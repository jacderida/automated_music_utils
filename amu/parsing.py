import os
import tempfile
import uuid
from amu import utils
from amu.audio import Mp3Tagger
from amu.audio import LameEncoder
from amu.audio import FlacEncoder
from amu.commands import AddArtworkCommand
from amu.commands import AddTagCommand
from amu.commands import DecodeAudioCommand
from amu.commands import EncodeWavCommand
from amu.commands import FetchReleaseCommand
from amu.commands import MoveAudioFileCommand
from amu.commands import RemoveTagCommand
from amu.commands import RipCdCommand
from amu.metadata import MaskReplacer
from amu.metadata import replace_forbidden_characters


class CommandParser(object):
    """ Responsible for parsing the string based command from the command line
        into a command object that can be executed.
    """
    def __init__(self, configuration_provider, cd_ripper, metadata_service, genre_selector):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._metadata_service = metadata_service
        self._mask_replacer = MaskReplacer()
        self._genre_selector = genre_selector

    def from_args(self, args):
        commands = {
            'rip': self._get_rip_command,
            'encode': self._get_encode_command,
            'decode': self._get_decode_command,
            'tag': self._get_tag_command,
            'fetch': self._get_fetch_command,
            'artwork': self._get_artwork_command,
            'mix': self._get_mix_command
        }
        return commands[args.command](args)

    def _get_mix_command(self, args):
        mix_args = AddTagCommandArgs.from_mix_command(args)
        parser = MixCommandParser(self._configuration_provider, Mp3Tagger())
        return parser.parse_mix_command(mix_args)

    def _get_artwork_command(self, args):
        if args.action == 'add' and args.type == 'mp3':
            if args.source:
                source = args.source
            else:
                source = os.getcwd().decode('utf-8')
            if args.destination:
                destination = args.destination
            else:
                destination = os.getcwd().decode('utf-8')
            parser = ArtworkCommandParser(self._configuration_provider, Mp3Tagger())
            return parser.parse_add_artwork_command(source, destination)

    def _get_decode_command(self, args):
        source = args.source if args.source else os.getcwd()
        destination = args.destination if args.destination else os.getcwd()
        parser = DecodeCommandParser(self._configuration_provider, FlacEncoder(self._configuration_provider))
        return parser.parse_decode_command(source, destination)

    def _get_fetch_command(self, args):
        command = FetchReleaseCommand(self._configuration_provider, self._metadata_service)
        command.discogs_id = int(args.discogs_id)
        return [command]

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
            collapse_index_tracks = True if args.collapse_index_tracks else False
            release_model = self._metadata_service.get_release_by_id(int(args.discogs_id), collapse_index_tracks)
            release_model.genre = self._genre_selector.select_genre([x.strip() for x in release_model.genre.split(',')])
            if not args.destination:
                destination = self._configuration_provider.get_releases_destination_with_mask_replaced(release_model, args.encoding_to)
        return self._get_encode_commands(args, destination, release_model)

    def _get_encode_commands(self, args, destination, release_model):
        if args.encoding_from == 'cd':
            commands = self._get_encode_cd_commands(args, destination, release_model)
        elif args.encoding_from == 'wav':
            commands = self._get_encode_wav_commands(args, destination, release_model)
        if args.keep_source:
            for command in commands:
                command.keep_source = True
        return commands

    def _get_tag_command(self, args):
        source = args.source if args.source else os.getcwd()
        tagger = self._get_tagger_based_on_format(args.format)
        tag_command_parser = TagCommandParser(self._configuration_provider, tagger, args.format)
        if args.discogs_id:
            commands = []
            collapse_index_tracks = True if args.collapse_index_tracks else False
            release_model = self._metadata_service.get_release_by_id(int(args.discogs_id), collapse_index_tracks)
            release_model.genre = self._genre_selector.select_genre([x.strip() for x in release_model.genre.split(',')])
            commands.extend(tag_command_parser.parse_from_release_model(source, release_model))
            move_file_parser = MoveAudioFileCommandParser(self._configuration_provider, args.format)
            commands.extend(move_file_parser.parse_from_release_model(
                source,
                self._configuration_provider.get_releases_destination_with_mask_replaced(release_model, args.format),
                release_model))
            return commands
        if args.action == 'remove':
            return tag_command_parser.parse_remove_tag_command(source)
        command_args = AddTagCommandArgs.from_args(args)
        command_args.source = source
        return tag_command_parser.parse_add_tag_command(command_args)

    def _get_encode_cd_commands(self, args, destination, release_model):
        commands = []
        encoder = self._get_encoder_based_on_destination_encoding(args.encoding_to)
        encode_command_parser = EncodeCommandParser(self._configuration_provider, self._cd_ripper, encoder, args.encoding_to)
        source = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        encode_commands = encode_command_parser.parse_cd_rip(source, destination)
        commands.extend(encode_commands)
        if release_model:
            # The first command is a rip cd command, which we don't need.
            commands.extend(self._get_release_tag_commands(args, encode_commands[1:], destination, release_model))
            move_file_parser = MoveAudioFileCommandParser(self._configuration_provider, args.encoding_to)
            commands.extend(move_file_parser.parse_from_encode_commands(encode_commands[1:], release_model))
        return commands

    def _get_encode_wav_commands(self, args, destination, release_model):
        if args.source:
            source = args.source
        else:
            source = os.getcwd().decode('utf-8')
        commands = []
        encoder = self._get_encoder_based_on_destination_encoding(args.encoding_to)
        encode_command_parser = EncodeCommandParser(self._configuration_provider, self._cd_ripper, encoder, args.encoding_to)
        encode_commands = encode_command_parser.parse_wav(source, destination)
        commands.extend(encode_commands)
        track_count = len(encode_commands)
        if track_count == 0:
            raise CommandParsingError('The source directory has no wavs to encode')
        if release_model:
            commands.extend(self._get_release_tag_commands(args, encode_commands, destination, release_model))
            commands.extend(self._get_add_artwork_commands(encode_commands))
            move_file_parser = MoveAudioFileCommandParser(self._configuration_provider, args.encoding_to)
            commands.extend(move_file_parser.parse_from_encode_commands(encode_commands, release_model))
        return commands

    def _get_encoder_based_on_destination_encoding(self, encoding_destination):
        if encoding_destination == 'mp3':
            return LameEncoder(self._configuration_provider)
        elif encoding_destination == 'flac':
            return FlacEncoder(self._configuration_provider)

    def _get_release_tag_commands(self, args, commands, destination, release_model):
        release_track_count = len(release_model.get_tracks())
        track_count = len(commands)
        if track_count != release_track_count:
            raise CommandParsingError(
                'The source has {0} tracks and the discogs release has {1}. The number of tracks on both must be the same.'.format(track_count, release_track_count))
        tagger = self._get_tagger_based_on_format(args.encoding_to)
        tag_command_parser = TagCommandParser(self._configuration_provider, tagger, args.encoding_to)
        if args.encoding_from == 'cd':
            return tag_command_parser.parse_from_release_model_with_empty_source(destination, release_model)
        return tag_command_parser.parse_from_release_model_with_sources(
            release_model, [x.destination for x in commands])

    def _get_tagger_based_on_format(self, format):
        if format == 'mp3':
            return Mp3Tagger()

    def _get_add_artwork_commands(self, encode_commands):
        artwork_command_parser = ArtworkCommandParser(self._configuration_provider, Mp3Tagger())
        return artwork_command_parser.parse_from_encode_commands(encode_commands)

class EncodeCommandParser(object):
    def __init__(self, configuration_provider, cd_ripper, encoder, encoding_destination):
        self._configuration_provider = configuration_provider
        self._cd_ripper = cd_ripper
        self._encoder = encoder
        self._encoding_destination = encoding_destination

    def parse_cd_rip(self, rip_destination, destination):
        if not rip_destination:
            raise CommandParsingError('The rip destination cannot be empty')
        if not destination:
            raise CommandParsingError('The destination cannot be empty')
        track_count = utils.get_number_of_tracks_on_cd()
        commands = []
        rip_cd_command = RipCdCommand(self._configuration_provider, self._cd_ripper)
        rip_cd_command.destination = rip_destination
        commands.append(rip_cd_command)
        for i in range(1, track_count + 1):
            command = EncodeWavCommand(self._configuration_provider, self._encoder)
            command.source = os.path.join(rip_destination, utils.get_track_name(i, "wav"))
            command.destination = os.path.join(destination, utils.get_track_name(i, self._encoding_destination))
            commands.append(command)
        return commands

    def parse_wav(self, source, destination):
        if not os.path.exists(source):
            raise CommandParsingError('The source directory or wav file must exist')
        if not destination:
            raise CommandParsingError('The destination cannot be empty')
        if os.path.isfile(source):
            return self._get_single_file_command(source, destination)
        return self._get_directory_command(source, destination)


    def _get_single_file_command(self, source, destination):
        if not destination.endswith(self._encoding_destination):
            raise CommandParsingError('If the source is a file, the destination must also be a file.')
        command = EncodeWavCommand(self._configuration_provider, self._encoder)
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
                        commands.append(self._get_encode_wav_command(full_source_directory, full_destination_directory, source_wav))
            else:
                for source_wav in [f for f in sorted(files) if f.endswith('.wav')]:
                    commands.append(self._get_encode_wav_command(root, destination, source_wav))
            break
        return commands

    def _get_encode_wav_command(self, source_directory, destination_directory, source_wav):
        command = EncodeWavCommand(self._configuration_provider, self._encoder)
        command.source = os.path.join(source_directory, source_wav)
        command.destination = os.path.join(destination_directory, os.path.splitext(source_wav)[0] + '.{0}'.format(self._encoding_destination))
        return command

class DecodeCommandParser(object):
    def __init__(self, configuration_provider, encoder):
        self._configuration_provider = configuration_provider
        self._encoder = encoder

    def parse_decode_command(self, source, destination):
        if not os.path.exists(source):
            raise CommandParsingError('The source directory or file must exist')
        if os.path.isfile(source):
            command = DecodeAudioCommand(self._configuration_provider, self._encoder)
            command.source = source
            command.destination = destination
            return [command]
        commands = []
        for root, directories, files in os.walk(source):
            if len(directories) > 0:
                for directory in sorted(directories):
                    full_source_directory = os.path.join(root, directory)
                    full_destination_directory = os.path.join(destination, directory)
                    for source_audio in [f for f in sorted(os.listdir(full_source_directory)) if f.endswith('.flac')]:
                        command = DecodeAudioCommand(self._configuration_provider, self._encoder)
                        command.source = os.path.join(full_source_directory, source_audio)
                        command.destination = os.path.join(full_destination_directory, os.path.splitext(source_audio)[0] + '.wav')
                        commands.append(command)
            else:
                for source_audio in [f for f in sorted(files) if f.endswith('.flac')]:
                    command = DecodeAudioCommand(self._configuration_provider, self._encoder)
                    command.source = os.path.join(root, source_audio)
                    command.destination = os.path.join(destination, os.path.splitext(source_audio)[0] + '.wav')
                    commands.append(command)
            break
        return commands

class TagCommandParser(object):
    def __init__(self, configuration_provider, tagger, source_format):
        self._configuration_provider = configuration_provider
        self._tagger = tagger
        self._source_format = source_format

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

        :source_path: The path where the encoded files will eventually be.
        :release_model: The release model with the metadata for the tags.
        :returns: A list of add tag commands.

        """
        commands = []
        track_number = 1
        for track in release_model.get_tracks():
            track_name = utils.get_track_name(track_number, self._source_format)
            full_source_path = os.path.join(source_path, track_name)
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
                    for source_file in [f for f in sorted(os.listdir(full_source_directory)) if f.endswith('.{0}'.format(self._source_format))]:
                        full_source_path = os.path.join(full_source_directory, source_file)
                        command = self._get_add_tag_command_from_release_model(full_source_path, release_model, tracks[i])
                        commands.append(command)
                        i += 1
            else:
                for source_file in [f for f in sorted(files) if f.endswith('.{0}'.format(self._source_format))]:
                    full_source = os.path.join(root, source_file)
                    command = self._get_add_tag_command_from_release_model(full_source, release_model, tracks[i])
                    commands.append(command)
                    i += 1
            break
        return commands

    def parse_add_tag_command(self, command_args):
        if os.path.isfile(command_args.source):
            return self._get_single_file_command(command_args)
        if command_args.track_total != 0:
            raise CommandParsingError('With a directory source, a track number and total override cannot be specified.')
        return self._get_directory_command(command_args)

    def parse_remove_tag_command(self, source):
        if os.path.isfile(source):
            command = RemoveTagCommand(self._configuration_provider, self._tagger)
            command.source = source
            return [command]
        commands = []
        for root, _, files in os.walk(source):
            audio_files = [f for f in files if f.endswith('.{0}'.format(self._source_format))]
            for audio_file in audio_files:
                command = RemoveTagCommand(self._configuration_provider, self._tagger)
                command.source = os.path.join(root, audio_file)
                commands.append(command)
        return commands

    def _get_single_file_command(self, command_args):
        command = self._get_add_tag_command(command_args.source, command_args)
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
                    source_files = [f for f in sorted(os.listdir(full_source_directory)) if f.endswith('.{0}'.format(self._source_format))]
                    track_total = len(source_files)
                    track_number = 1
                    for source_file in source_files:
                        full_source_path = os.path.join(full_source_directory, source_file)
                        command_args.disc_number = disc_number
                        command_args.disc_total = disc_total
                        command = self._get_add_tag_command(full_source_path, command_args)
                        command.track_number = track_number
                        command.track_total = track_total
                        commands.append(command)
                        track_number += 1
                    disc_number += 1
            else:
                source_files = [f for f in sorted(files) if f.endswith('.{0}'.format(self._source_format))]
                track_total = len(source_files)
                track_number = 1
                for source_file in source_files:
                    full_source_path = os.path.join(root, source_file)
                    command = self._get_add_tag_command(full_source_path, command_args)
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
        command_args.album_artist = release_model.artist
        command_args.album = release_model.title
        command_args.title = track.title
        command_args.year = release_model.original_release.year if release_model.original_release != None else release_model.year
        command_args.genre = release_model.genre
        command_args.comment = u'{0} ({1})'.format(release_model.label, release_model.catno)
        command_args.track_number = track.track_number
        command_args.track_total = track.track_total
        command_args.disc_number = track.disc_number
        command_args.disc_total = track.disc_total
        return self._get_add_tag_command(source, command_args)

    def _get_add_tag_command(self, source, command_args):
        command = AddTagCommand(self._configuration_provider, self._tagger)
        command.source = source
        command.artist = command_args.artist
        command.album_artist = command_args.album_artist
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
    def __init__(self, configuration_provider, source_format):
        self._configuration_provider = configuration_provider
        self._source_format = source_format

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
        source = os.path.dirname(encode_commands[0].source)
        commands.extend(
            self._get_move_cover_command(source, os.path.dirname(encode_commands[0].destination)))
        return commands

    def parse_from_release_model(self, source, destination, release_model):
        if not os.path.isdir(source):
            raise CommandParsingError('The source must be a directory.')
        if not os.path.isdir(destination):
            os.makedirs(destination)
        commands = []
        for root, directories, files in os.walk(source):
            directory_len = len(directories)
            if directory_len > 0:
                commands.extend(self._get_multi_cd_parse_from_release_model_commands(release_model, root, directories, destination))
            else:
                commands.extend(self._get_single_directory_parse_from_release_model_commands(release_model, root, files, destination))
            break
        return commands

    def _get_move_cover_command(self, source, destination):
        images = [
            f for f in [
                image for image in os.listdir(source) if image.endswith('.jpg') or image.endswith('.png')
            ] if f.startswith('cover')
        ]
        if len(images) > 0:
            command = MoveAudioFileCommand(self._configuration_provider)
            command.source = os.path.join(source, images[0])
            command.destination = os.path.join(destination, images[0])
            return [command]
        return []

    def _get_multi_cd_parse_from_release_model_commands(self, release_model, source_path, directories, destination):
        i = 0
        tracks = release_model.get_tracks()
        commands = []
        commands.extend(self._get_move_cover_command(source_path, destination))
        for directory in sorted(directories):
            full_source_directory = os.path.join(source_path, directory)
            source_files = [f for f in sorted(os.listdir(full_source_directory)) if f.endswith('.{0}'.format(self._source_format))]
            for source_file in source_files:
                command = MoveAudioFileCommand(self._configuration_provider)
                command.source = os.path.join(source_path, directory, source_file)
                command.destination = self._get_full_destination_from_track(os.path.join(destination, directory), tracks[i])
                commands.append(command)
                i += 1
        return commands

    def _get_single_directory_parse_from_release_model_commands(self, release_model, source_path, source_files, destination):
        i = 0
        tracks = release_model.get_tracks()
        audio_files = [f for f in sorted(source_files) if f.endswith('.{0}'.format(self._source_format))]
        commands = []
        while i < len(audio_files):
            command = MoveAudioFileCommand(self._configuration_provider)
            command.source = os.path.join(source_path, audio_files[i])
            command.destination = self._get_full_destination_from_track(destination, tracks[i])
            commands.append(command)
            i += 1
        commands.extend(self._get_move_cover_command(source_path, destination))
        return commands

    def _get_destination(self, destination, track):
        directory_path = os.path.dirname(destination)
        extension = os.path.splitext(destination)[1][1:] # ignore the . that splitext returns
        track_number = ''
        if track.track_number < 10:
            track_number = '0' + str(track.track_number)
        else:
            track_number = track.track_number
        return u'{0}/{1} - {2}.{3}'.format(
            directory_path, track_number, replace_forbidden_characters(track.title), extension)

    def _get_full_destination_from_track(self, destination, track):
        track_number = ''
        if track.track_number < 10:
            track_number = '0' + str(track.track_number)
        else:
            track_number = track.track_number
        return os.path.join(destination, '{0} - {1}.{2}'.format(track_number, replace_forbidden_characters(track.title), self._source_format))

class ArtworkCommandParser(object):
    def __init__(self, configuration_provider, tagger):
        self._configuration_provider = configuration_provider
        self._tagger = tagger

    def parse_add_artwork_command(self, source, destination):
        cover = self._get_cover_path(source)
        if os.path.isdir(destination):
            commands = []
            for root, directories, files in os.walk(destination):
                directory_len = len(directories)
                if directory_len > 0:
                    commands.extend(self._get_multi_cd_commands(root, directories, cover))
                else:
                    commands.extend(self._get_single_cd_commands(files, cover, destination))
                break
            return commands
        return [self._get_add_artwork_command(source, destination)]

    def parse_from_encode_commands(self, encode_commands):
        commands = []
        source = os.path.dirname(encode_commands[0].source)
        images = [
            f for f in [
                image for image in os.listdir(source) if image.endswith('.jpg') or image.endswith('.png')
            ] if f.startswith('cover')
        ]
        if len(images) == 0:
            return commands
        cover = os.path.join(source, images[0])
        for encode_command in encode_commands:
            command = AddArtworkCommand(self._configuration_provider, self._tagger)
            command.source = cover
            command.destination = encode_command.destination
            commands.append(command)
        return commands

    def _get_multi_cd_commands(self, root, directories, cover):
        commands = []
        for directory in directories:
            full_destination_directory = os.path.join(root, directory)
            audio_files = [f for f in os.listdir(full_destination_directory) if f.endswith('.mp3')]
            for audio_file in audio_files:
                commands.append(self._get_add_artwork_command(cover, os.path.join(full_destination_directory, audio_file)))
        return commands

    def _get_single_cd_commands(self, files, cover, destination):
        commands = []
        audio_files = [f for f in files if f.endswith('.mp3')]
        for audio_file in audio_files:
            commands.append(self._get_add_artwork_command(cover, os.path.join(destination, audio_file)))
        return commands

    def _get_cover_path(self, source):
        if os.path.isdir(source):
            images = [f for f in [image for image in os.listdir(source) if image.endswith('.jpg') or image.endswith('.png')] if f.startswith('cover')]
            if len(images) == 0:
                raise CommandParsingError('The source directory contains no cover jpg or png.')
            return os.path.join(source, images[0])
        return source

    def _get_add_artwork_command(self, source, destination):
        command = AddArtworkCommand(self._configuration_provider, self._tagger)
        command.source = source
        command.destination = destination
        return command

class MixCommandParser(object):
    def __init__(self, configuration_provider, tagger):
        self._configuration_provider = configuration_provider
        self._tagger = tagger

    def parse_mix_command(self, add_tag_args):
        if not add_tag_args.source:
            raise ValueError('A value must be supplied for the source.')
        if os.path.isfile(add_tag_args.source):
            add_tag_command = self._get_add_tag_command(add_tag_args, add_tag_args.source, add_tag_args.title, 1, 1)
            move_file_command = self._get_move_file_command(add_tag_args.source, os.path.basename(add_tag_args.source))
            return [add_tag_command, move_file_command]
        part = 1
        commands = []
        mix_files = [x for x in sorted(os.listdir(add_tag_args.source)) if x.endswith('.mp3')]
        for mix_file in mix_files:
            source_path = os.path.join(add_tag_args.source, mix_file)
            commands.append(self._get_add_tag_command(
                add_tag_args,
                source_path,
                u'{0} Part {1}'.format(add_tag_args.title.decode('utf-8'), part),
                part,
                len(mix_files)))
            commands.append(self._get_move_file_command(source_path, mix_file))
            part += 1
        return commands

    def _get_add_tag_command(self, add_tag_args, source, title, track_number, track_total):
        command = AddTagCommand(self._configuration_provider, self._tagger)
        command.source = source
        command.artist = add_tag_args.artist
        command.album_artist = add_tag_args.artist
        command.album = add_tag_args.album
        command.title = title
        command.year = add_tag_args.year
        command.comment = add_tag_args.comment
        command.genre = 'Mixes'
        command.track_number = track_number
        command.track_total = track_total
        command.disc_number = 1
        command.disc_total = 1
        return command

    def _get_move_file_command(self, source, destination_file):
        command = MoveAudioFileCommand(self._configuration_provider)
        command.source = source
        command.destination = os.path.join(self._configuration_provider.get_mixes_destination(), destination_file)
        return command

class AddTagCommandArgs(object):
    def __init__(self):
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

    @staticmethod
    def from_args(args):
        command_args = AddTagCommandArgs()
        command_args.source = AddTagCommandArgs._get_value_from_args(args.source)
        command_args.artist = AddTagCommandArgs._get_value_from_args(args.artist)
        command_args.album_artist = AddTagCommandArgs._get_value_from_args(args.album_artist)
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
    def from_mix_command(args):
        command_args = AddTagCommandArgs()
        command_args.source = AddTagCommandArgs._get_value_from_args(args.source)
        command_args.artist = AddTagCommandArgs._get_value_from_args(args.artist)
        command_args.album = AddTagCommandArgs._get_value_from_args(args.album)
        command_args.title = AddTagCommandArgs._get_value_from_args(args.title)
        command_args.year = AddTagCommandArgs._get_value_from_args(args.year)
        command_args.comment = AddTagCommandArgs._get_value_from_args(args.comment)
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
