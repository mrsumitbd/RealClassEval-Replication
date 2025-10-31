import numpy as np
from viscm.bezierbuilder.curve import curve_method
from matplotlib.lines import Line2D

class SingleBezierCurveModel:

    def __init__(self, control_point_model, method='CatmulClark'):
        self.method = curve_method[method]
        self.control_point_model = control_point_model
        x, y = self.get_bezier_points()
        self.bezier_curve = Line2D(x, y)
        self.trigger = self.control_point_model.trigger
        self.trigger.add_callback(self._refresh)

    def get_bezier_points(self, num=200):
        return self.get_bezier_points_at(np.linspace(0, 1, num))

    def get_bezier_points_at(self, at, grid=1000):
        xp, yp, _ = self.control_point_model.get_control_points()
        return compute_bezier_points(xp, yp, at, self.method, grid=grid)

    def _refresh(self):
        x, y = self.get_bezier_points()
        self.bezier_curve.set_data(x, y)