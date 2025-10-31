
class _TaskConfig:

    def __init__(self, name, priority, description=None):
        self.name = name
        self.priority = priority
        self.description = description

    def to_dict(self):
        return {
            'name': self.name,
            'priority': self.priority,
            'description': self.description
        }

    @classmethod
    def from_dict(cls, config):
        return cls(
            name=config.get('name'),
            priority=config.get('priority'),
            description=config.get('description')
        )
