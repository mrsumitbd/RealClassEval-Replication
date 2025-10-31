class TargetSetter:

    def __init__(self, obj, key):
        self.obj = obj
        self.key = key

    def set_value(self, value):
        self.obj[self.key] = value