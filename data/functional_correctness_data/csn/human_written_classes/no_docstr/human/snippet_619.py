class HighlightPoint2DView:

    def __init__(self, ax, highlight_point_model):
        self.ax = ax
        self.highlight_point_model = highlight_point_model
        _, ap, bp = self.highlight_point_model.get_Jpapbp()
        self.marker = self.ax.plot([ap], [bp], 'y.', mew=3)[0]
        self.highlight_point_model.trigger.add_callback(self._refresh)

    def _refresh(self):
        _, ap, bp = self.highlight_point_model.get_Jpapbp()
        self.marker.set_data([ap], [bp])
        self.ax.figure.canvas.draw()