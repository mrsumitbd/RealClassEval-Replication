class Ref:
    """
    Represents the !Ref tag in YAML, used to reference other configuration paths.
    """

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'!Ref {self.path}'