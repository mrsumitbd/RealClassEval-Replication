class TaskParams:
    """A parameter object that encaptulates parameters sending to
    task executors. This would makes the output of workers, especially
    in the web interface much cleaner (issue #259)"""

    def __init__(self, name, global_def, task, sos_dict, tags):
        self.name = name
        self.global_def = global_def
        self.task = task
        self.sos_dict = sos_dict
        self.tags = tags
        if 'CONFIG' in self.sos_dict and '__builtins__' in self.sos_dict['CONFIG']:
            self.sos_dict['CONFIG'].pop('__builtins__')

    def __repr__(self):
        return self.name