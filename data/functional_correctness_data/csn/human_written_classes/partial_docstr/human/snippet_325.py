class Command:
    name = ''
    pre_info_message = ''
    post_info_message = ''
    priority = None
    description = ''
    options_definitions = []
    arguments_definitions = []
    aliases = []

    def __init__(self, ui=None, docker_backend=None, docker_object=None, buffer=None, size=None):
        """

        :param ui:
        :param docker_backend:
        :param docker_object:
        :param buffer:
        """
        logger.debug('command %r initialized: ui=%r, docker_backend=%r, docker_object=%r, buffer=%r', self.name, ui, docker_backend, docker_object, buffer)
        self.ui = ui
        self.docker_backend = docker_backend
        self.docker_object = docker_object
        self.buffer = buffer
        self.size = size
        self.argument_processor = ArgumentProcessor(self.options_definitions, self.arguments_definitions)
        self.arguments = None

    def process_args(self, arguments):
        """

        :param arguments: dict
        :return:
        """
        given_arguments = self.argument_processor.process(arguments)
        logger.info('given arguments = %s', given_arguments)
        self.arguments = CommandArgumentsGetter(given_arguments)

    def run(self):
        raise NotImplementedError()