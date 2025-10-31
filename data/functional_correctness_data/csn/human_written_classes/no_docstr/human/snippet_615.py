from matplotlib.lines import Line2D
from viscm.bezierbuilder.curve import curve_method
import numpy as np

class TwoBezierCurveModel:

    def __init__(self, control_point_model, method='CatmulClark'):
        self.method = curve_method[method]
        self.control_point_model = control_point_model
        x, y = self.get_bezier_points()
        self.bezier_curve = Line2D(x, y)
        self.trigger = self.control_point_model.trigger
        self.trigger.add_callback(self._refresh)

    def get_bezier_points(self, num=200):
        return self.get_bezier_points_at(np.linspace(0, 1, num))

    def get_bezier_points_at(self, at, grid=256):
        at = np.asarray(at)
        if at.ndim == 0:
            at = np.array([at])
        low_mask = at < 0.5
        high_mask = at >= 0.5
        xp, yp, fixed = self.control_point_model.get_control_points()
        assert fixed is not None
        low_xp = xp[:fixed + 1]
        low_yp = yp[:fixed + 1]
        high_xp = xp[fixed:]
        high_yp = yp[fixed:]
        low_al = compute_arc_length(low_xp, low_yp, self.method).max()
        high_al = compute_arc_length(high_xp, high_yp, self.method).max()
        sf = min(low_al, high_al) / max(low_al, high_al)
        high_at = at[high_mask]
        low_at = at[low_mask]
        if high_al < low_al:
            high_at = high_at * 2 - 1
            low_at = (0.5 - (0.5 - low_at) * sf) * 2
        else:
            high_at = (0.5 + (high_at - 0.5) * sf) * 2 - 1
            low_at = low_at * 2
        low_points = compute_bezier_points(low_xp, low_yp, low_at, self.method, grid=grid)
        high_points = compute_bezier_points(high_xp, high_yp, high_at, self.method, grid=grid)
        out = np.concatenate([low_points, high_points], 1)
        return out

    def _refresh(self):
        x, y = self.get_bezier_points()
        self.bezier_curve.set_data(x, y)