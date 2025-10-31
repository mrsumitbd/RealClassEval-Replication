class PythonHandler:
    key = '__python__'

    def __init__(self, config):
        self.config = config

    def __call__(self, name, props):
        statements = props.pop(self.key)
        exec(statements, globals(), {key: self.config for key in ['C', 'cfg', 'config']})
        return props