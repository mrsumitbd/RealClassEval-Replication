class Variable:
    """
    Class representing an E+ mtd variable.

    Parameters
    ----------
    ref: str
    variable_id: int
    unit: str
    """

    def __init__(self, ref, variable_id, unit):
        self.ref = ref
        self.variable_id = variable_id
        self.unit = unit
        self.meters_l = []

    def link_meter(self, meter):
        """
        Add meter to this variable.

        Parameters
        ----------
        meter: str
        """
        if meter in self.meters_l:
            raise RuntimeError('Meter already linked.')
        self.meters_l = []