class Data:

    def __init__(self, pos=None, x=None, y=None, edge_index=None, surf=None, sample_name=None):
        self.pos = pos
        self.x = x
        self.y = y
        self.edge_index = edge_index
        self.surf = surf
        self.sample_name = sample_name

    def __repr__(self):
        return f'\nData(x={self._format_attr(self.x)}, edge_index={self._format_attr(self.edge_index)}, y={self._format_attr(self.y)}, pos={self._format_attr(self.pos)}, surf={self._format_attr(self.surf)}, sample_name={self._format_attr(self.sample_name)})'

    def _format_attr(self, attr):
        if attr is None:
            return 'None'
        elif hasattr(attr, 'shape'):
            return f"[{', '.join(map(str, attr.shape))}]"
        else:
            return str(attr)