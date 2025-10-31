class RectangularFinExchanger:
    """Class representing a plate-fin heat exchanger with straight rectangular
    fins. All parameters are also attributes.

    Parameters
    ----------
    fin_height : float
        The total distance between the two metal plates sandwiching the fins
        and holding them together (abbreviated `h`), [m]
    fin_thickness : float
        The thickness of the material the fins were formed from
        (abbreviated `t`), [m]
    fin_spacing : float
        The unit cell spacing from one fin to the next; the space between the
        sides of two fins plus one thickness (abbreviated `s`), [m]
    length : float, optional
        The total length of the flow passage of the plate-fin exchanger
        (abbreviated `L`), [m]
    width : float, optional
        The total width of the space the fins are in; this is also
        :math:`N_{fins}\\times s` (abbreviated `W`), [m]
    layers : int, optional
        The number of layers in the plate-fin exchanger; note these HX almost
        always single-pass only, [-]
    plate_thickness : float, optional
        The thickness of the metal separator between layers, [m]
    flow : str, optional
        One of 'counterflow', 'crossflow', or 'parallelflow'

    Attributes
    ----------
    channel_height : float
        The height of the channel the fluid flows in
        :math:`\\text{channel height } = \\text{fin height} - \\text{fin thickness}`, [m]
    channel_width : float
        The width of the channel the fluid flows in
        :math:`\\text{channel width } = \\text{fin spacing} - \\text{fin thickness}`, [m]
    fin_count : int
        The number of fins per unit length of the layer,
        :math:`\\text{fin count} = \\frac{1}{\\text{fin spacing}}`, [1/m]
    blockage_ratio : float
        The fraction of the layer which is blocked to flow by the fins,
        :math:`\\text{blockage ratio} = \\frac{s\\cdot h - s\\cdot t - t(h-t)}{s\\cdot h}`,
        [m]
    A_channel : float
        Flow area of a single channel in a single layer,
        :math:`\\text{channel area} = (s-t)(h-t)`, [m]
    P_channel : float
        Wetted perimeter of a single channel in a single layer,
        :math:`\\text{channel perimeter} = 2(s-t) + 2(h-t)`, [m]
    Dh : float
        Hydraulic diameter of a single channel in a single layer,
        :math:`D_{hydraulic} = \\frac{4 A_{channel}}{P_{channel}}`, [m]
    layer_thickness : float
        The thickness of a single layer - the sum of a fin height and
        a plate thickness, [m]
    layer_fin_count : int
        The number of fins in a layer; rounded to the nearest whole fin, [-]
    A_HX_layer : float
        The surface area including fins for heat transfer in one layer of the
        HX, [m^2]
    A_HX : float
        The total surface area of the heat exchanger with all layers combined,
        [m^2]
    height : float
        The height of all the layers of the heat exchanger combined, plus one
        extra plate thickness, [m]
    volume : float
        The product of the height, width, and length of the HX, [m^3]
    A_specific_HX : float
        The specific surface area of the heat exchanger - square meters per
        meter cubed, [m^3]

    Notes
    -----
    The only required parameters are the fin geometry itself; `fin_height`,
    `fin_thickness`, and `fin_spacing`.

    Examples
    --------
    >>> PFE = RectangularFinExchanger(0.03, 0.001, 0.012)
    >>> PFE.Dh
    0.01595

    References
    ----------
    .. [1] Yang, Yujie, and Yanzhong Li. "General Prediction of the Thermal
       Hydraulic Performance for Plate-Fin Heat Exchanger with Offset Strip
       Fins." International Journal of Heat and Mass Transfer 78 (November 1,
       2014): 860-70. doi:10.1016/j.ijheatmasstransfer.2014.07.060.
    .. [2] Sheik Ismail, L., R. Velraj, and C. Ranganayakulu. "Studies on
       Pumping Power in Terms of Pressure Drop and Heat Transfer
       Characteristics of Compact Plate-Fin Heat Exchangers-A Review."
       Renewable and Sustainable Energy Reviews 14, no. 1 (January 2010):
       478-85. doi:10.1016/j.rser.2009.06.033.
    """

    def __init__(self, fin_height, fin_thickness, fin_spacing, length=None, width=None, layers=None, plate_thickness=None, flow='crossflow'):
        self.h = self.fin_height = fin_height
        self.t = self.fin_thickness = fin_thickness
        self.s = self.fin_spacing = fin_spacing
        self.L = self.length = length
        self.W = self.width = width
        self.layers = layers
        self.flow = flow
        self.plate_thickness = plate_thickness
        self.channel_height = self.fin_height - self.fin_thickness
        self.channel_width = self.fin_spacing - self.fin_thickness
        self.fin_count = 1.0 / self.fin_spacing
        self.blockage_ratio = (self.s * self.h - self.s * self.t - (self.h - self.t) * self.t) / (self.s * self.h)
        self.A_channel = (self.s - self.t) * (self.h - self.t)
        self.P_channel = 2 * (self.s - self.t) + 2 * (self.h - self.t)
        self.Dh = 4 * self.A_channel / self.P_channel
        self.set_overall_geometry()

    def set_overall_geometry(self):
        if self.plate_thickness:
            self.layer_thickness = self.plate_thickness + self.fin_height
        if self.length and self.width:
            self.layer_fin_count = round(self.fin_count * self.width, 0)
            if hasattr(self, 'SA_fin'):
                self.A_HX_layer = self.layer_fin_count * self.SA_fin * self.length
            else:
                self.A_HX_layer = self.P_channel * self.length * self.layer_fin_count
            if self.layers:
                self.A_HX = self.layers * self.A_HX_layer
                if self.plate_thickness:
                    self.height = self.layer_thickness * self.layers + self.plate_thickness
                    self.volume = self.length * self.width * self.height
                    self.A_specific_HX = self.A_HX / self.volume