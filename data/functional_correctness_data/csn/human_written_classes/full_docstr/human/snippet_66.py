class ArgumentProcessor:
    """
    responsible for parsing given list of arguments
    """

    def __init__(self, options, arguments):
        """
        :param options: list of options
        :param arguments: list of arguments
        """
        self.given_arguments = {}
        self.options = {}
        for a in options:
            self.options[a.name] = a
            self.given_arguments[normalize_arg_name(a.name)] = a.default
            for alias in a.aliases:
                self.options[alias] = a
        for o in arguments:
            self.given_arguments[normalize_arg_name(o.name)] = o.default
        self.arguments = arguments
        logger.info('arguments = %s', arguments)
        logger.info('options = %s', options)

    def process(self, argument_list):
        """
        :param argument_list: list of str, input from user
        :return: dict:
            {"cleaned_arg_name": "value"}
        """
        arg_index = 0
        for a in argument_list:
            opt_and_val = a.split('=', 1)
            opt_name = opt_and_val[0]
            try:
                argument = self.options[opt_name]
            except KeyError:
                try:
                    argument = self.arguments[arg_index]
                except IndexError:
                    logger.error('option/argument %r not specified', a)
                    raise NoSuchOptionOrArgument('No such option or argument: %r' % opt_name)
            logger.info('argument found: %s', argument)
            safe_arg_name = normalize_arg_name(argument.name)
            logger.info('argument is available under name %r', safe_arg_name)
            if isinstance(argument, Argument):
                arg_index += 1
                value = (a,)
            else:
                try:
                    value = (opt_and_val[1],)
                except IndexError:
                    value = tuple()
            arg_val = argument.action(*value)
            logger.info('argument %r has value %r', safe_arg_name, arg_val)
            self.given_arguments[safe_arg_name] = arg_val
        return self.given_arguments