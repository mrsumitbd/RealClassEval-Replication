from matplotlib.lines import Line2D

class BezierCurveView:

    def __init__(self, ax, bezier_curve_model):
        self.ax = ax
        self.bezier_curve_model = bezier_curve_model
        self.canvas = self.ax.figure.canvas
        x, y = self.bezier_model.get_bezier_points()
        self.bezier_curve = Line2D(x, y)
        self.ax.add_line(self.bezier_curve)
        self.bezier_curve_model.trigger.add_callback(self._refresh)
        self._refresh()

    def _refresh(self):
        x, y = self.bezier_curve_model.get_bezier_points()
        self.bezier_curve.set_data(x, y)
        self.canvas.draw()