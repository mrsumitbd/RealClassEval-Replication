class PlateExchanger:
    """Class representing a plate heat exchanger with sinusoidal ridges.
    All parameters are also attributes.

    Parameters
    ----------
    amplitude : float
        Half the height of the wave of the ridges, [m]
    wavelength : float
        Distance between the bottoms of two of the ridges (sometimes called
        pitch), [m]
    chevron_angle : float, optional
        Angle of the plate corrugations with respect to the vertical axis
        (the direction of flow if the plates were straight), between 0 and
        90, [degrees]
    chevron_angles : tuple(2), optional
        Many plate exchangers use two alternating patterns; for those cases
        provide tuple of the two angles for that situation and the argument
        `chevron_angle` is ignored, [degrees]
    width : float, optional
        Width of the plates in the heat exchanger, between the gaskets, [m]
    length : float, optional
        Length of the heat exchanger as measured from one port to the other,
        excluding the diameter of the ports themselves (little useful heat
        transfer happens there), [m]
    thickness : float, optional
        Thickness of the metal making up the plates, [m]
    d_port : float, optional
        The diameter of the ports in the plates, [m]
    plates : int, optional
        The number of plates in the heat exchanger, including the two not
        used for heat transfer at the beginning and end [-]

    Attributes
    ----------
    chevron_angles : tuple(2)
        The two specified angles (repeated value if only one specified), [degrees]
    chevron_angle : float
        The averaged angle of the chevrons, [degrees]
    inclination_angle : float
        90 - `chevron_angle`, used in many publications instead of `chevron_angle`,
        [degrees]
    plate_corrugation_aspect_ratio : float
        The aspect ratio of the corrugations
        :math:`\\gamma = \\frac{4a}{\\lambda}`, [-]
    plate_enlargement_factor : float
        The extra surface area multiplier as compared to a flat plate
        caused the corrugations, [-]
    D_eq : float
        Equivalent diameter of the channels, :math:`D_{eq} = 4a` [m]
    D_hydraulic : float
        Hydraulic diameter of the channels, :math:`D_{hyd} = \\frac{4a}{\\phi}` [m]
    length_port : float
        Port center to port center along the direction of flow, [m]
    A_plate_surface : float
        The surface area of one plate in the heat exchanger, including the
        extra due to corrugations (excluding the bit between the ports),
        :math:`A_p = L\\cdot W\\cdot \\phi` [m^2]
    A_heat_transfer : float
        The total surface area available for heat transfer in the exchanger,
        the multiple of `A_plate_surface` by the number of plates after
        removing the two on the edges, [m^2]
    A_channel_flow : float
        The area for the fluid to flow in one channel, :math:`W\\cdot b` [m^2]
    channels : int
        The number of plates minus one, [-]
    channels_per_fluid : int
        Half the number of total channels, [-]

    Notes
    -----
    Only wavelength and amplitude are required as inputs to this function.

    Examples
    --------
    >>> PlateExchanger(amplitude=5E-4, wavelength=3.7E-3, length=1.2, width=.3,
    ... d_port=.05, plates=51)
    <Plate heat exchanger, amplitude=0.0005 m, wavelength=0.0037 m, chevron_angles=45/45 degrees, area enhancement factor=1.16119, width=0.3 m, length=1.2 m, port diameter=0.05 m, heat transfer area=20.4833 m^2, 51 plates>

    References
    ----------
    .. [1] Amalfi, Raffaele L., Farzad Vakili-Farahani, and John R. Thome.
       "Flow Boiling and Frictional Pressure Gradients in Plate Heat Exchangers.
       Part 1: Review and Experimental Database." International Journal of
       Refrigeration 61 (January 2016): 166-84. doi:10.1016/j.ijrefrig.2015.07.010.
    """

    def __repr__(self):
        s = '<Plate heat exchanger, amplitude={:g} m, wavelength={:g} m, chevron_angles={} degrees, area enhancement factor={:g}'.format(self.a, self.wavelength, '/'.join([str(i) for i in self.chevron_angles]), self.plate_enlargement_factor)
        if self.width and self.length:
            s += f', width={self.width:g} m, length={self.length:g} m'
        if self.d_port:
            s += f', port diameter={self.d_port:g} m'
        if self.plates:
            s += f', heat transfer area={self.A_heat_transfer:g} m^2, {self.plates:g} plates>'
        else:
            s += '>'
        return s

    @property
    def plate_exchanger_identifier(self):
        """Method to create an identifying string in format 'L' + wavelength +
        'A' + amplitude + 'B' + chevron angle-chevron angle.

        Wavelength and amplitude are specified in units of mm and rounded to two
        decimal places.
        """
        wave_rounded = round(self.wavelength * 1000, 2)
        amplitude_rounded = round(self.amplitude * 1000, 2)
        a1 = self.chevron_angles[0]
        a2 = self.chevron_angles[1]
        s = f'L{wave_rounded}A{amplitude_rounded}B{a1}-{a2}'
        return s

    def __init__(self, amplitude, wavelength, chevron_angle=45, chevron_angles=None, width=None, length=None, thickness=None, d_port=None, plates=None):
        self.amplitude = self.a = amplitude
        self.b = 2 * self.amplitude
        self.wavelength = self.pitch = wavelength
        if chevron_angles is not None:
            self.chevron_angles = chevron_angles
            self.chevron_angle = self.beta = 0.5 * (chevron_angles[0] + chevron_angles[1])
        else:
            self.chevron_angle = self.beta = chevron_angle
            self.chevron_angles = (chevron_angle, chevron_angle)
        self.inclination_angle = 90 - self.chevron_angle
        self.plate_corrugation_aspect_ratio = self.gamma = 4 * self.a / self.wavelength
        self.plate_enlargement_factor = plate_enlargement_factor(self.amplitude, self.wavelength)
        self.D_eq = 4 * self.amplitude
        self.D_hydraulic = 4 * self.amplitude / self.plate_enlargement_factor
        if width is not None:
            self.width = width
        if length is not None:
            self.length = length
        if thickness is not None:
            self.thickness = thickness
        if d_port is not None:
            self.d_port = d_port
        if plates is not None:
            self.plates = plates
        if d_port is not None and length is not None:
            self.length_port = length + d_port
        if width is not None and length is not None:
            self.A_plate_surface = length * width * self.plate_enlargement_factor
            if plates is not None:
                self.A_heat_transfer = (plates - 2) * self.A_plate_surface
        if width is not None:
            self.A_channel_flow = self.width * self.b
        if plates is not None:
            self.channels = self.plates - 1
            self.channels_per_fluid = 0.5 * self.channels