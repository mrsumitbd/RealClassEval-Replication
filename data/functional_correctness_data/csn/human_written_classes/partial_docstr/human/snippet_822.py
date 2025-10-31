import numpy as np

class GeometryStorage:
    """Abstract base class for geometries"""

    def __init__(self, coord_vars, node_count):
        self.coord_vars = coord_vars
        self.node_count = node_count
        self.errors = []
        self.geometry = None

    def check_geometry(self):
        invalid_vars = []
        for coord_var in self.coord_vars:
            if not np.issubdtype(coord_var, float):
                invalid_vars.append(coord_var.name)
        if invalid_vars:
            self.errors.append(f'The following geometry variables have non-numeric contents: {invalid_vars}')

    def _split_mulitpart_geometry(self):
        arr_extents_filt = self.part_node_count[self.part_node_count > 0]
        splits = np.split(np.vstack(self.coord_vars).T, arr_extents_filt.cumsum()[:-1])
        return splits