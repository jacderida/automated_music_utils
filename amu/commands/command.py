""" Base command that provides functionality common to all commands. """


class Command(object):
    """ Base command that provides functionality common to all commands. """

    def validate(self):
        """ Validates the command before execution. """
        pass

    def execute(self):
        """ Executes the command. """
        pass

class CommandValidationError(Exception):
    def __init__(self, message):
        super(CommandValidationError, self).__init__(message)
        self.message = message
