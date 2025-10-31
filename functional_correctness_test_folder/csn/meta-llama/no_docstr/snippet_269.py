
class _TaskConfig:

    def __init__(self, task_name, task_type, task_params):
        self.task_name = task_name
        self.task_type = task_type
        self.task_params = task_params

    def to_dict(self):
        return {
            'task_name': self.task_name,
            'task_type': self.task_type,
            'task_params': self.task_params
        }

    @classmethod
    def from_dict(cls, config):
        return cls(
            task_name=config['task_name'],
            task_type=config['task_type'],
            task_params=config['task_params']
        )
