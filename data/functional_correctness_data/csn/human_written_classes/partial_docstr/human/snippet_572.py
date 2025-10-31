from cmath import sqrt as csqrt
from math import acos, acosh, asin, atan, cos, degrees, isclose, log, log1p, pi, radians, sin, sqrt, tan

class AirCooledExchanger:
    """Class representing the geometry of an air cooled heat exchanger with
    one or more tube bays, fans, or bundles.
    All parameters are also attributes.

    The minimum information required to describe an air cooler is as follows:

    * `tube_rows`
    * `tube_passes`
    * `tubes_per_row`
    * `tube_length`
    * `tube_diameter`
    * `fin_thickness`

    Two of `angle`, `pitch`, `pitch_parallel`, and `pitch_normal`
    (`pitch_ratio` may take the place of `pitch`)

    Either `fin_diameter` or `fin_height`.
    Either `fin_density` or `fin_interval`.

    Parameters
    ----------
    tube_rows : int
        Number of tube rows per bundle, [-]
    tube_passes : int
        Number of tube passes (times the fluid travels across one tube length),
        [-]
    tubes_per_row : float
        Number of tubes per row per bundle, [-]
    tube_length : float
        Total length of the tube bundle tubes, [m]
    tube_diameter : float
        Diameter of the bare tube, [m]
    fin_thickness : float
        Thickness of the fins, [m]
    angle : float, optional
        Angle of the tube layout, [degrees]
    pitch : float, optional
        Shortest distance between tube centers; defined in relation to the
        flow direction only, [m]
    pitch_parallel : float, optional
        Distance between tube center along a line parallel to the flow;
        has been called `longitudinal` pitch, `pp`, `s2`, `SL`, and `p2`, [m]
    pitch_normal : float, optional
        Distance between tube centers in a line 90° to the line of flow;
        has been called the `transverse` pitch, `pn`, `s1`, `ST`, and `p1`, [m]
    pitch_ratio : float, optional
        Ratio of the pitch to bare tube diameter, [-]
    fin_diameter : float, optional
        Outer diameter of each tube after including the fin on both sides,
        [m]
    fin_height : float, optional
        Height above bare tube of the tube fins, [m]
    fin_density : float, optional
        Number of fins per meter of tube, [1/m]
    fin_interval : float, optional
        Space between each fin, including the thickness of one fin at its
        base, [m]
    parallel_bays : int, optional
        Number of bays in the unit, [-]
    bundles_per_bay : int, optional
        Number of tube bundles per bay, [-]
    fans_per_bay : int, optional
        Number of fans per bay, [-]
    corbels : bool, optional
        Whether or not the air cooler has corbels, which increase the air
        velocity by adding half a tube to the sides for the case of
        non-rectangular tube layouts, [-]
    tube_thickness : float, optional
        Thickness of the bare metal tubes, [m]
    fan_diameter : float, optional
        Diameter of air cooler fan, [m]

    Attributes
    ----------
    bare_length : float
        Length of bare tube between two fins
        :math:`\\text{bare length} = \\text{fin interval} - t_{fin}`, [m]
    tubes_per_bundle : float
        Total number of tubes per bundle
        :math:`N_{tubes/bundle} = N_{tubes/row} \\cdot N_{rows}`, [-]
    tubes_per_bay : float
        Total number of tubes per bay
        :math:`N_{tubes/bay} = N_{tubes/bundle} \\cdot N_{bundles/bay}`, [-]
    tubes : float
        Total number of tubes in all bundles in all bays combined
        :math:`N_{tubes} = N_{tubes/bay} \\cdot N_{bays}`, [-]

    pitch_diagonal : float
        Distance between tube centers in a diagonal line between one normal
        tube and one parallel tube;
        :math:`s_D = \\left[s_L^2 + \\left(\\frac{s_T}{2}\\right)^2\\right]^{0.5}`,
        [m]

    A_bare_tube_per_tube : float
        Area of the bare tube including the portion hidden by the fin per
        tube :math:`A_{bare,total/tube} = \\pi D_{tube} L_{tube}`, [m^2]
    A_bare_tube_per_row : float
        Area of the bare tube including the portion hidden by the fin per
        tube row
        :math:`A_{bare,total/row} = \\pi D_{tube} L_{tube} N_{tubes/row}`, [m^2]
    A_bare_tube_per_bundle : float
        Area of the bare tube including the portion hidden by the fin per
        bundle :math:`A_{bare,total/bundle} = \\pi D_{tube} L_{tube}
        N_{tubes/bundle}`, [m^2]
    A_bare_tube_per_bay : float
        Area of the bare tube including the portion hidden by the fin per
        bay :math:`A_{bare,total/bay} = \\pi D_{tube} L_{tube} N_{tubes/bay}`,
        [m^2]
    A_bare_tube : float
        Area of the bare tube including the portion hidden by the fin per
        in all bundles and bays combined :math:`A_{bare,total} = \\pi D_{tube}
        L_{tube} N_{tubes}`, [m^2]

    A_tube_showing_per_tube : float
        Area of the bare tube which is exposed per tube :math:`A_{bare,
        showing/tube} = \\pi D_{tube} L_{tube}  \\left(1 - \\frac{t_{fin}}
        {\\text{fin interval}} \\right)`, [m^2]
    A_tube_showing_per_row : float
        Area of the bare tube which is exposed per tube row, [m^2]
    A_tube_showing_per_bundle : float
        Area of the bare tube which is exposed per bundle, [m^2]
    A_tube_showing_per_bay : float
        Area of the bare tube which is exposed per bay, [m^2]
    A_tube_showing : float
        Area of the bare tube which is exposed in all bundles and bays
        combined, [m^2]

    A_per_fin : float
        Surface area per fin :math:`A_{fin} = 2 \\frac{\\pi}{4} (D_{fin}^2 -
        D_{tube}^2) + \\pi D_{fin} t_{fin}`, [m^2]
    A_fin_per_tube : float
        Surface area of all fins per tube
        :math:`A_{fin/tube} = N_{fins/m} L_{tube} A_{fin}`, [m^2]
    A_fin_per_row : float
        Surface area of all fins per row, [m^2]
    A_fin_per_bundle : float
        Surface area of all fins per bundle, [m^2]
    A_fin_per_bay : float
        Surface area of all fins per bay, [m^2]
    A_fin : float
        Surface area of all fins in all bundles and bays combined, [m^2]

    A_per_tube : float
        Surface area of combined finned and non-fined area exposed for heat
        transfer per tube :math:`A_{tube} = A_{bare, showing/tube}
        + A_{fin/tube}`, [m^2]
    A_per_row : float
        Surface area of combined finned and non-finned area exposed for heat
        transfer per tube row, [m^2]
    A_per_bundle : float
        Surface area of combined finned and non-finned area exposed for heat
        transfer per tube bundle, [m^2]
    A_per_bay : float
        Surface area of combined finned and non-finned area exposed for heat
        transfer per bay, [m^2]
    A : float
        Surface area of combined finned and non-finned area exposed for heat
        transfer in all bundles and bays combined, [m^2]
    A_increase : float
        Ratio of actual surface area to bare tube surface area
        :math:`A_{increase} = \\frac{A_{tube}}{A_{bare, total/tube}}`, [-]

    A_tube_flow : float
        The area for the fluid to flow in one tube, :math:`\\pi/4\\cdot D_i^2`,
        [m^2]
    A_tube_flow_per_row : float
        The area for the fluid to flow in one row, :math:`\\pi/4\\cdot D_i^2 N_{tubes/row}`,
        [m^2]
    A_tube_flow_per_bundle : float
        The area for the fluid to flow in one bundle, :math:`\\pi/4\\cdot D_i^2 N_{tubes/bundle}`,
        [m^2]
    A_tube_flow_per_bay : float
        The area for the fluid to flow in one bay, :math:`\\pi/4\\cdot D_i^2 N_{tubes/bay}`,
        [m^2]
    A_tube_flow_total : float
        The area for the fluid to flow in all tubes combined, as if there
        were a single pass [m^2]
    channels : int
        The number of tubes the fluid flows through at the inlet header, [-]

    tube_volume_per_tube : float
        Fluid volume per tube inside :math:`V_{tube, flow} = \\frac{\\pi}{4}
        D_{i}^2 L_{tube}`, [m^3]
    tube_volume_per_row : float
        Fluid volume of tubes per row, [m^3]
    tube_volume_per_bundle : float
        Fluid volume of tubes per bundle, [m^3]
    tube_volume_per_bay : float
        Fluid volume of tubes per bay, [m^3]
    tube_volume : float
        Fluid volume of tubes in all bundles and bays combined, [m^3]


    A_diagonal_per_bundle : float
        Air flow area along the diagonal plane per bundle
        :math:`A_d = 2 N_{tubes/row} L_{tube} (P_d - D_{tube} - 2 N_{fins/m} h_{fin} t_{fin}) + A_\\text{extra,side}`, [m^2]
    A_normal_per_bundle : float
        Air flow area along the normal (transverse) plane; this is normally
        the minimum flow area, except for some staggered configurations
        :math:`A_t = N_{tubes/row} L_{tube} (P_t - D_{tube} - 2 N_{fins/m} h_{fin} t_{fin}) + A_\\text{extra,side}`, [m^2]
    A_min_per_bundle : float
        Minimum air flow area per bundle; this is the characteristic area for
        velocity calculation in most finned tube convection correlations
        :math:`A_{min} = min(A_d, A_t)`, [m^2]
    A_min_per_bay : float
        Minimum air flow area per bay, [m^2]
    A_min : float
        Minimum air flow area, [m^2]

    A_face_per_bundle : float
        Face area per bundle :math:`A_{face} = P_{T} (1+N_{tubes/row})
        L_{tube}`; if corbels are used, add 0.5 to tubes/row instead of 1,
        [m^2]
    A_face_per_bay : float
        Face area per bay, [m^2]
    A_face : float
        Total face area, [m^2]
    flow_area_contraction_ratio : float
        Ratio of `A_min` to `A_face`, [-]


    Notes
    -----

    Examples
    --------
    >>> from scipy.constants import inch
    >>> AC = AirCooledExchanger(tube_rows=4, tube_passes=4, tubes_per_row=56, tube_length=10.9728,
    ... tube_diameter=1*inch, fin_thickness=0.013*inch, fin_density=10/inch,
    ... angle=30, pitch=2.5*inch, fin_height=0.625*inch, tube_thickness=0.00338,
    ... bundles_per_bay=2, parallel_bays=3, corbels=True)


    References
    ----------
    .. [1] Schlunder, Ernst U, and International Center for Heat and Mass
       Transfer. Heat Exchanger Design Handbook. Washington:
       Hemisphere Pub. Corp., 1983.
    """

    def __repr__(self):
        attributes = ', '.join((f'{slot}={getattr(self, slot)!r}' for slot in self.model_inputs))
        return f'{self.__class__.__name__}({attributes})'

    def __hash__(self):
        return hash(tuple((getattr(self, slot) for slot in self.model_inputs)))
    model_inputs = ('tube_rows', 'tube_passes', 'tubes_per_row', 'tube_length', 'tube_diameter', 'fin_thickness', 'angle', 'pitch', 'pitch_parallel', 'pitch_normal', 'fin_diameter', 'fin_height', 'fin_density', 'fin_interval', 'parallel_bays', 'bundles_per_bay', 'fans_per_bay', 'corbels', 'tube_thickness', 'fan_diameter')

    def __init__(self, tube_rows, tube_passes, tubes_per_row, tube_length, tube_diameter, fin_thickness, angle=None, pitch=None, pitch_parallel=None, pitch_normal=None, pitch_ratio=None, fin_diameter=None, fin_height=None, fin_density=None, fin_interval=None, parallel_bays=1, bundles_per_bay=1, fans_per_bay=1, corbels=False, tube_thickness=None, fan_diameter=None):
        self.tube_rows = tube_rows
        self.tube_passes = tube_passes
        self.tubes_per_row = tubes_per_row
        self.tube_length = tube_length
        self.tube_diameter = tube_diameter
        self.fin_thickness = fin_thickness
        self.fan_diameter = fan_diameter
        if pitch_ratio is not None:
            if pitch is not None:
                pitch = self.tube_diameter * pitch_ratio
            else:
                raise ValueError('Specify only one of `pitch_ratio` or `pitch`')
        angle, pitch, pitch_parallel, pitch_normal = pitch_angle_solver(angle=angle, pitch=pitch, pitch_parallel=pitch_parallel, pitch_normal=pitch_normal)
        self.angle = angle
        self.pitch = pitch
        self.pitch_ratio = pitch / self.tube_diameter
        self.pitch_parallel = pitch_parallel
        self.pitch_normal = pitch_normal
        self.pitch_diagonal = sqrt(pitch_parallel ** 2 + (0.5 * pitch_normal) ** 2)
        if fin_diameter is None and fin_height is None:
            raise ValueError('Specify only one of `fin_diameter` or `fin_height`')
        elif fin_diameter is not None:
            fin_height = 0.5 * (fin_diameter - tube_diameter)
        elif fin_height is not None:
            fin_diameter = tube_diameter + 2.0 * fin_height
        self.fin_height = fin_height
        self.fin_diameter = fin_diameter
        if fin_density is None and fin_interval is None:
            raise ValueError('Specify only one of `fin_density` or `fin_interval`')
        elif fin_density is not None:
            fin_interval = 1.0 / fin_density
        elif fin_interval is not None:
            fin_density = 1.0 / fin_interval
        self.fin_interval = fin_interval
        self.fin_density = fin_density
        self.parallel_bays = parallel_bays
        self.bundles_per_bay = bundles_per_bay
        self.fans_per_bay = fans_per_bay
        self.corbels = corbels
        self.tube_thickness = tube_thickness
        if self.fin_interval:
            self.bare_length = self.fin_interval - self.fin_thickness
        else:
            self.bare_length = None
        self.tubes_per_bundle = self.tubes_per_row * self.tube_rows
        self.tubes_per_bay = self.tubes_per_bundle * self.bundles_per_bay
        self.tubes = self.tubes_per_bay * self.parallel_bays
        self.A_bare_tube_per_tube = pi * self.tube_diameter * self.tube_length
        self.A_bare_tube_per_row = self.A_bare_tube_per_tube * self.tubes_per_row
        self.A_bare_tube_per_bundle = self.A_bare_tube_per_tube * self.tubes_per_bundle
        self.A_bare_tube_per_bay = self.A_bare_tube_per_tube * self.tubes_per_bay
        self.A_bare_tube = self.A_bare_tube_per_tube * self.tubes
        self.A_tube_showing_per_tube = pi * self.tube_diameter * self.tube_length * (1.0 - self.fin_thickness / self.fin_interval)
        self.A_tube_showing_per_row = self.A_tube_showing_per_tube * self.tubes_per_row
        self.A_tube_showing_per_bundle = self.A_tube_showing_per_tube * self.tubes_per_bundle
        self.A_tube_showing_per_bay = self.A_tube_showing_per_tube * self.tubes_per_bay
        self.A_tube_showing = self.A_tube_showing_per_tube * self.tubes
        self.A_per_fin = 2.0 * pi / 4.0 * (self.fin_diameter ** 2 - self.tube_diameter ** 2) + pi * self.fin_diameter * self.fin_thickness
        self.A_fin_per_tube = self.fin_density * self.tube_length * self.A_per_fin
        self.A_fin_per_row = self.A_fin_per_tube * self.tubes_per_row
        self.A_fin_per_bundle = self.A_fin_per_tube * self.tubes_per_bundle
        self.A_fin_per_bay = self.A_fin_per_tube * self.tubes_per_bay
        self.A_fin = self.A_fin_per_tube * self.tubes
        self.A_per_tube = self.A_tube_showing_per_tube + self.A_fin_per_tube
        self.A_per_row = self.A_tube_showing_per_row + self.A_fin_per_row
        self.A_per_bundle = self.A_tube_showing_per_bundle + self.A_fin_per_bundle
        self.A_per_bay = self.A_tube_showing_per_bay + self.A_fin_per_bay
        self.A = self.A_tube_showing + self.A_fin
        self.A_increase = self.A / self.A_bare_tube
        A_extra = 0.0
        self.A_diagonal_per_bundle = 2.0 * self.tubes_per_row * self.tube_length * (self.pitch_diagonal - self.tube_diameter - 2.0 * fin_density * self.fin_height * self.fin_thickness) + A_extra
        self.A_normal_per_bundle = self.tubes_per_row * self.tube_length * (self.pitch_normal - self.tube_diameter - 2.0 * fin_density * self.fin_height * self.fin_thickness) + A_extra
        self.A_min_per_bundle = min(self.A_diagonal_per_bundle, self.A_normal_per_bundle)
        self.A_min_per_bay = self.A_min_per_bundle * self.bundles_per_bay
        self.A_min = self.A_min_per_bay * self.parallel_bays
        i = 0.5 if self.corbels else 1.0
        self.A_face_per_bundle = self.pitch_normal * self.tube_length * (self.tubes_per_row + i)
        self.A_face_per_bay = self.A_face_per_bundle * self.bundles_per_bay
        self.A_face = self.A_face_per_bay * self.parallel_bays
        self.flow_area_contraction_ratio = self.A_min / self.A_face
        if self.tube_thickness is not None:
            self.Di = self.tube_diameter - self.tube_thickness * 2.0
            self.A_tube_flow = pi / 4.0 * self.Di * self.Di
            self.A_tube_flow_per_row = self.A_tube_flow * self.tubes_per_row
            self.A_tube_flow_per_bundle = self.A_tube_flow * self.tubes_per_bundle
            self.A_tube_flow_per_bay = self.A_tube_flow * self.tubes_per_bay
            self.A_tube_flow_total = self.A_tube_flow * self.tubes
            self.tube_volume_per_tube = self.A_tube_flow * self.tube_length
            self.tube_volume_per_row = self.tube_volume_per_tube * self.tubes_per_row
            self.tube_volume_per_bundle = self.tube_volume_per_tube * self.tubes_per_bundle
            self.tube_volume_per_bay = self.tube_volume_per_tube * self.tubes_per_bay
            self.tube_volume = self.tube_volume_per_tube * self.tubes
        else:
            self.Di = None
            self.A_tube_flow = None
            self.tube_volume_per_tube = None
            self.tube_volume_per_row = None
            self.tube_volume_per_bundle = None
            self.tube_volume_per_bay = None
            self.tube_volume = None
        if self.tube_rows % self.tube_passes == 0:
            self.channels = self.tubes_per_bundle / self.tube_passes
        else:
            self.channels = self.tubes_per_row
        if self.angle == 30:
            self.pitch_str = 'triangular'
            self.pitch_class = 'staggered'
        elif self.angle == 60:
            self.pitch_str = 'rotated triangular'
            self.pitch_class = 'staggered'
        elif self.angle == 45:
            self.pitch_str = 'rotated square'
            self.pitch_class = 'in-line'
        elif self.angle == 90:
            self.pitch_str = 'square'
            self.pitch_class = 'in-line'
        else:
            self.pitch_str = 'custom'
            self.pitch_class = 'custom'