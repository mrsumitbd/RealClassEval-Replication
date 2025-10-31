class Meter:
    """
    Class describing an E+ mtd meter.

    Parameters
    ----------
    ref: str
    unit: str
    kwargs: dict
    """

    def __init__(self, ref, unit, **kwargs):
        self.ref = ref
        self.unit = unit
        self.kwargs = kwargs
        self.variables_l = []

    def link_variable(self, variable):
        """
        Add variable to this meter.

        Parameters
        ----------
        variable: str
        """
        if variable in self.variables_l:
            raise RuntimeError('Variable already linked.')
        self.variables_l.append(variable)