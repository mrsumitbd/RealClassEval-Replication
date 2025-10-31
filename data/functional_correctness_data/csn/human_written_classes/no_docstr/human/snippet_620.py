from viscm.minimvc import Trigger

class HighlightPointModel:

    def __init__(self, cmap_model, point):
        self._cmap_model = cmap_model
        self._point = point
        self.trigger = Trigger()
        self._cmap_model.trigger.add_callback(self.trigger.fire)

    def get_point(self):
        return self._point

    def set_point(self, point):
        self._point = point
        self.trigger.fire()

    def get_Jpapbp(self):
        return self._cmap_model.get_Jpapbp_at_point(self._point)