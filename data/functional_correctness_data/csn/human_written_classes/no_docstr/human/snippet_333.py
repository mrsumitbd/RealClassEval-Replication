class CommandArgumentsGetter:

    def __init__(self, given_arguments):
        self.given_arguments = given_arguments

    def set_argument(self, arg_name, value):
        self.given_arguments[arg_name] = value

    def __getattr__(self, item):
        try:
            return self.given_arguments[item]
        except KeyError:
            logger.error('no argument/option defined: %r', item)
            raise AttributeError('No such option or argument: %r' % item)