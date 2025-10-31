class dbannotation:
    """
    Object with information about annotation: containg one dict that
    store all features for each database type
    """

    def __init__(self, na):
        self.ann = {}

    def add_db_ann(self, ida, ndba):
        self.ann[ida] = ndba