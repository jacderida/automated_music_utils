""" Base command that provides functionality common to all commands. """


class Command(object):
    """ Base command that provides functionality common to all commands. """

    def validate(self):
        """ Validates the command before execution. """
        pass

    def execute(self):
        """ Executes the command. """
        pass
