import numpy as np

class CellBlock:

    def __init__(self, cell_type: str, data: list | np.ndarray, tags: list[str] | None=None):
        self.type = cell_type
        self.data = data
        if cell_type.startswith('polyhedron'):
            self.dim = 3
        else:
            self.data = np.asarray(self.data)
            self.dim = topological_dimension[cell_type]
        self.tags = [] if tags is None else tags

    def __repr__(self):
        items = ['meshio CellBlock', f'type: {self.type}', f'num cells: {len(self.data)}', f'tags: {self.tags}']
        return '<' + ', '.join(items) + '>'

    def __len__(self):
        return len(self.data)