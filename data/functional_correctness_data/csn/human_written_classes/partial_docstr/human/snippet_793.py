class style:

    def __init__(self, name, _ctx, **kwargs):
        """Graph styling.

        The default style is used for edges. When text is set to None,
        no id label is displayed.
        """
        self.name = name
        self._ctx = _ctx
        if not _ctx:
            return
        self.background = _ctx.color(0.45, 0.45, 0.5, 1.0)
        self.traffic = _ctx.color(0.0, 0.0, 0.0, 0.07)
        self.fill = _ctx.color(0.0, 0.0, 0.0, 0.1)
        self.stroke = _ctx.color(0.8, 0.8, 0.8, 0.75)
        self.strokewidth = 0.5
        self.text = _ctx.color(1.0, 1.0, 1.0, 0.85)
        self.font = 'Calibri'
        self.fontsize = 10
        self.textwidth = 100
        self.align = 1
        self.depth = True
        self.graph_background = graph_background
        self.graph_traffic = graph_traffic
        self.node = node
        self.node_label = node_label
        self.edges = edges
        self.edge = edge
        self.edge_arrow = edge_arrow
        self.edge_label = edge_label
        self.path = path
        for attr in kwargs:
            if attr in self.__dict__:
                self.__dict__[attr] = kwargs[attr]
        if self.depth:
            try:
                global colors
                colors = _ctx.ximport('colors')
            except:
                self.depth = False

    def copy(self, name=None):
        s = style(self.name, self._ctx)
        for attr in self.__dict__:
            v = self.__dict__[attr]
            if isinstance(v, self.fill.__class__):
                v = v.copy()
            s.__dict__[attr] = v
        if name is not None:
            s.name = name
        return s