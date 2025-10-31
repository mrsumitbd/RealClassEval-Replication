class TransformerDing0:
    """
    Transformers are essentially voltage converters, which
    enable to change between voltage levels based on the usage.

    Attributes
    ----------
    id_db : :obj:`int`
        id according to database table
    grid : :class:`~.ding0.core.network.grids.MVGridDing0`
        The MV grid that this ring is to be a part of.
    v_level : :obj:`float`
        voltage level [kV]
    s_max_a : :obj:`float`
        rated power (long term)	[kVA]
    s_max_b : :obj:`float`
        rated power (short term)	        
    s_max_c : :obj:`float`
        rated power (emergency)	
    phase_angle : :obj:`float`
        phase shift angle
    tap_ratio: :obj:`float`
        off nominal turns ratio
    """

    def __init__(self, **kwargs):
        self.id_db = kwargs.get('id_db', None)
        self.grid = kwargs.get('grid', None)
        self.v_level = kwargs.get('v_level', None)
        self.s_max_a = kwargs.get('s_max_longterm', None)
        self.s_max_b = kwargs.get('s_max_shortterm', None)
        self.s_max_c = kwargs.get('s_max_emergency', None)
        self.phase_angle = kwargs.get('phase_angle', None)
        self.tap_ratio = kwargs.get('tap_ratio', None)
        self.r_pu = kwargs.get('r_pu', None)
        self.x_pu = kwargs.get('x_pu', None)

    @property
    def network(self):
        """
        Getter for the overarching :class:`~.ding0.core.network.NetworkDing0`
        object.

        Returns
        -------
        :class:`~.ding0.core.network.NetworkDing0`
        """
        return self.grid.network

    def z(self, voltage_level=None):
        """
        Calculates the complex impedance in Ohm related to voltage_level. If voltage_level is not inserted, the secondary
        voltage of the transformer is chosen as a default.
        :param voltage_level:
        voltage in [kV]
        :return: Z_tr in [Ohm]
        """
        if voltage_level is None:
            voltage_level = self.v_level
        Z_tr = (self.r_pu + self.x_pu * 1j) * voltage_level ** 2 / self.s_max_a * 1000
        return Z_tr

    def __repr__(self):
        return '_'.join(['Transformer', repr(self.grid), str(self.id_db)])