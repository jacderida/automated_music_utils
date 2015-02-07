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
