class Axis:

    def __init__(self, axis):
        self._axis = axis

    def set_parameter(self, name=None, value=None):
        if name is None or value is None:
            return
        for parameter in self._axis.__dict__.values():
            if getattr(parameter, 'name', None) == name:
                parameter.value = value

    def __str__(self):
        data = Tree()
        data[self._axis.name] = {'Start': self._axis.start.value, 'Stop': self._axis.stop.value, 'Number of Points': self._axis.npoints.value, 'Gaussian': self._axis.gaussian.value, 'Lorentzian': self._axis.lorentzian.value}
        return prettify(data)

    def _repr_pretty_(self, p, cycle):
        p.text(str(self) if not cycle else '...')