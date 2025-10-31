class URDFTree:
    """
    Utility class to represent a URDF tree, only used here
    Still very experimental, this class will change in the future
    """

    def __init__(self, name):
        self.name = name
        self.children_links = {}

    def __repr__(self):
        return 'URDF Link: {};\n'.format(self.name)