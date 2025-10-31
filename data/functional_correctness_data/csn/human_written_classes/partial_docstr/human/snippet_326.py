import shlex

class Commander:
    """
    Responsible for managing commands: it's up to workers to do the commands actually.
    """

    def __init__(self, ui, docker_backend):
        self.ui = ui
        self.docker_backend = docker_backend
        self.modifier_keys_pressed = []
        logger.debug('available commands: %s', commands_mapping)

    def get_command(self, command_input, docker_object=None, buffer=None, size=None):
        """
        return command instance which is the actual command to be executed

        :param command_input: str, command name and its args: "command arg arg2=val opt"
        :param docker_object:
        :param buffer:
        :param size: tuple, so we can call urwid.keypress(size, ...)
        :return: instance of Command
        """
        logger.debug('get command for command input %r', command_input)
        if not command_input:
            return
        if command_input[0] in ['/']:
            command_name = command_input[0]
            unparsed_command_args = shlex.split(command_input[1:])
        else:
            command_input_list = shlex.split(command_input)
            command_name = command_input_list[0]
            unparsed_command_args = command_input_list[1:]
        try:
            CommandClass = commands_mapping[command_name]
        except KeyError:
            logger.info('no such command: %r', command_name)
            raise NoSuchCommand('There is no such command: %s' % command_name)
        else:
            cmd = CommandClass(ui=self.ui, docker_backend=self.docker_backend, docker_object=docker_object, buffer=buffer, size=size)
            cmd.process_args(unparsed_command_args)
            return cmd

    def get_command_input_by_key(self, key):
        logger.debug('get command input for key %r', key)
        modifier_keys = ['g']
        inp = ''.join(self.modifier_keys_pressed) + key
        try:
            command_input = self.ui.current_buffer.get_keybinds()[inp]
        except KeyError:
            if key in modifier_keys:
                self.modifier_keys_pressed.append(key)
                logger.info('modifier keys pressed: %s', self.modifier_keys_pressed)
                return
            else:
                logger.info('no such keybind: %r', inp)
                self.modifier_keys_pressed.clear()
                raise KeyNotMapped('No such keybind: %r.' % inp)
        else:
            self.modifier_keys_pressed.clear()
            return command_input