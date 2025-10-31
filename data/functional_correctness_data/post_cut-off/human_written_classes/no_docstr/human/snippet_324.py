from module.config.utils import deep_get, DEFAULT_TIME, deep_set, filepath_config, path_to_arg, dict_to_kv, get_server_next_update, nearest_future

class Function:

    def __init__(self, data):
        self.enable = deep_get(data, keys='Scheduler.Enable', default=False)
        self.command = deep_get(data, keys='Scheduler.Command', default='Unknown')
        self.next_run = deep_get(data, keys='Scheduler.NextRun', default=DEFAULT_TIME)

    def __str__(self):
        enable = 'Enable' if self.enable else 'Disable'
        return f'{self.command} ({enable}, {str(self.next_run)})'
    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False
        if self.command == other.command and self.next_run == other.next_run:
            return True
        else:
            return False