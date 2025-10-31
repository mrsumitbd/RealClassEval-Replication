class Props:

    def __init__(self, instance) -> None:
        self.prop_map = [('x', int), ('y', int), ('width', int), ('height', int), ('data', lambda x: x), ('labels', instance.assign_labels)]
        self.prop_map_title = [('x', int), ('y', int), ('_text', str)]
        self.prop_map_legend = [('x', int), ('y', int), ('deltax', int), ('alignment', str), ('boxAnchor', str), ('fontSize', int), ('strokeWidth', int), ('dy', int), ('dx', int), ('dxTextSpace', int), ('deltay', int), ('columnMaximum', int), ('variColumn', int), ('deltax', int), ('fontName', str), ('colorNamePairs', list)]
        self.prop_map_legend1 = [('x', int), ('y', int)]
        self.prop_map_bars = [('strokeWidth', int)]
        self.prop_map_barLabels = [('nudge', int), ('fontSize', int), ('fontName', str)]
        self.prop_map_categoryAxis = [('visibleTicks', int), ('strokeWidth', int), ('tickShift', int), ('labelAxisMode', str)]
        self.prop_map_categoryAxis_labels = [('angle', int), ('dy', int), ('fontSize', int), ('boxAnchor', str), ('fontName', str), ('textAnchor', str)]
        self.prop_map_slices = [('strokeWidth', int), ('labelRadius', float), ('poput', int), ('fontName', str), ('fontSize', int), ('strokeDashArray', str)]

    @staticmethod
    def add_prop(prop_map, data):
        prop_map += data