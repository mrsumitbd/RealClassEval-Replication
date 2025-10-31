class AxisDefinitionFactory:
    """Creates a set of axis definitions, making sure to recognize default axes
    (weight and width) and also keeping track of indices of custom axes.

    From looking at a Glyphs file with only one custom axis, it looks like
    when there is an "Axes" customParameter, the axis design locations are
    stored in `weightValue` for the first axis (regardless of whether it is
    a weight axis, `widthValue` for the second axis, etc.
    """

    def __init__(self):
        self.axis_index = -1

    def get(self, tag=None, name='Custom'):
        self.axis_index += 1
        design_loc_key = self._design_loc_key()
        if tag is None:
            if self.axis_index == 0:
                tag = 'XXXX'
            else:
                tag = 'XXX%d' % self.axis_index
        if tag == 'wght':
            return AxisDefinition(tag, name, design_loc_key, 100.0, 'weight', 'weightClass', 400.0)
        if tag == 'wdth':
            return AxisDefinition(tag, name, design_loc_key, 100.0, 'width', 'widthClass', 100.0)
        return AxisDefinition(tag, name, design_loc_key, 0.0, None, None, 0.0)

    def _design_loc_key(self):
        return self.axis_index