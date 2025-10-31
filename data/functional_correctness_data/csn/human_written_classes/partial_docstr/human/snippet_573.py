from cmath import sqrt as csqrt
from math import acos, acosh, asin, atan, cos, degrees, isclose, log, log1p, pi, radians, sin, sqrt, tan

class HelicalCoil:
    """Class representing a helical coiled tube, as are found in many heated
    tanks and some small nuclear reactors. All parameters are also attributes.

    One set of the following parameters is required; inner tube diameter is
    optional.

        * Tube outer diameter, coil outer diameter, pitch, number of coil turns
        * Tube outer diameter, coil outer diameter, pitch, height
        * Tube outer diameter, coil outer diameter, number of coil turns, height

    Parameters
    ----------
    Dt : float
        Outer diameter of the tube wound to make up the helical spiral, [m]
    Do : float
        Diameter of the spiral as measured from the center of the coil on one
        side to the center of the coil on the other side, [m]
    Do_total : float, optional
        Diameter of the spiral as measured from one edge of the tube to the
        other edge; equal to Do + Dt; either `Do` or `Do_total` may be
        specified and the other will be calculated [m]
    pitch : float, optional
        Height change from one coil to the next as measured from the middles
        of the tube, [m]
    H : float, optional
        Height of the spiral, as measured from the middle of the bottom of the
        tube to the middle of the top of the tube, [m]
    H_total : float, optional
        Height of the spiral as measured from one edge of the tube to the other
        edge; equal to `H_total` + `Dt`; either may be specified and the other
        will be calculated [m]
    N : float, optional
        Number of coil turns; may be specified along with `pitch` instead of
        specifying `H` or `H_total`, [-]
    Di : float, optional
        Inner diameter of the tube; if specified, inside and annulus properties
        will be calculated, [m]

    Attributes
    ----------
    tube_circumference : float
        Circumference of the tube as measured though its center, not inner or
        outer edges;  :math:`C = \\pi D_o`, [m]
    tube_length : float
        Length of tube used to make the helical coil;
        :math:`L = \\sqrt{(\\pi D_o\\cdot N)^2 + H^2}`, [m]
    surface_area : float
        Surface area of the outer surface of the helical coil;
        :math:`A_t = \\pi D_t L`, [m^2]
    inner_surface_area : float
        Surface area of the inner surface of the helical coil; calculated if
        `Di` is supplied; :math:`A_{inside} = \\pi D_i L`, [m^2]
    inlet_area : float
        Area of the inlet to the helical coil; calculated if
        `Di` is supplied; :math:`A_{inlet} = \\frac{\\pi}{4} D_i^2`, [m^2]
    inner_volume : float
        Volume of the tube as would be filled by a fluid, useful for weight
        calculations; calculated if `Di` is supplied;
        :math:`V_{inside} = A_i L`, [m^3]
    annulus_area : float
        Area of the annulus (wall of the pipe); calculated if `Di` is supplied;
        :math:`A_a = \\frac{\\pi}{4} (D_t^2 - D_i^2)`, [m^2]
    annulus_volume : float
        Volume of the annulus (wall of the pipe); calculated if `Di`
        is supplied, useful for weight calculations; :math:`V_a = A_a L`, [m^3]
    total_volume : float
        Total volume occupied by the pipe and the fluid inside it;
        :math:`V = D_t L`, [m^3]
    helix_angle : float
        Angle between the pitch and coil diameter; used in some calculations;
        :math:`\\alpha = \\arctan \\left(\\frac{p_t}{\\pi D_o}\\right)`, [radians]
    curvature : float
        Coil curvature, useful in some calculations;
        :math:`\\delta = \\frac{D_t}{D_o[1 + 4\\pi^2 \\tan^2(\\alpha)]}`, [-]

    Notes
    -----
    `Do` must be larger than `Dt`.

    Examples
    --------
    >>> C1 = HelicalCoil(Do=30, H=20, pitch=5, Dt=2)
    >>> C1.N, C1.tube_length, C1.surface_area
    (4.0, 377.5212621504738, 2372.0360474917497)

    Same coil, with the inputs one would physically measure from the coil,
    and a specified inlet diameter:

    >>> C1 = HelicalCoil(Do_total=32, H_total=22, pitch=5, Dt=2, Di=1.8)
    >>> C1.N, C1.tube_length, C1.surface_area
    (4.0, 377.5212621504738, 2372.0360474917497)
    >>> C1.inner_surface_area, C1.inlet_area, C1.inner_volume, C1.total_volume, C1.annulus_volume
    (2134.832442742575, 2.5446900494077327, 960.6745992341587, 1186.0180237458749, 225.3434245117162)

    References
    ----------
    .. [1] El-Genk, Mohamed S., and Timothy M. Schriener. "A Review and
       Correlations for Convection Heat Transfer and Pressure Losses in
       Toroidal and Helically Coiled Tubes." Heat Transfer Engineering 0, no. 0
       (June 7, 2016): 1-28. doi:10.1080/01457632.2016.1194693.
    """

    def __repr__(self):
        s = f'<Helical coil, total height={self.H_total} m, total outer diameter={self.Do_total} m, tube outer diameter={self.Dt} m, number of turns={self.N}, pitch={self.pitch} m'
        if self.Di:
            s += f', inside diameter {self.Di} m'
        s += '>'
        return s

    def __init__(self, Dt, Do=None, pitch=None, H=None, N=None, H_total=None, Do_total=None, Di=None):
        if H_total is not None:
            H = H_total - Dt
        if Do_total is not None:
            Do = Do_total - Dt
        self.Do = Do
        self.Dt = Dt
        self.Do_total = self.Do + self.Dt
        if N is not None and pitch is not None:
            self.N = N
            self.pitch = pitch
            self.H = N * pitch
        elif N is not None and H is not None:
            self.N = N
            self.H = H
            self.pitch = self.H / N
            if self.pitch < self.Dt:
                raise ValueError('Pitch is too small - tubes are colliding')
        elif H is not None and pitch is not None:
            self.pitch = pitch
            self.H = H
            self.N = self.H / self.pitch
            if self.pitch < self.Dt:
                raise ValueError('Pitch is too small - tubes are colliding; pitch must be larger than tube diameter.')
        if self.H is not None:
            self.H_total = self.Dt + self.H
        if self.Dt > self.Do:
            raise ValueError('Tube diameter is larger than helix outer diameter - not feasible.')
        self.tube_circumference = pi * self.Do
        self.tube_length = sqrt((self.tube_circumference * self.N) ** 2 + self.H ** 2)
        self.surface_area = self.tube_length * pi * self.Dt
        self.helix_angle = atan(self.pitch / (pi * self.Do))
        self.curvature = self.Dt / self.Do / (1.0 + 4 * pi ** 2 * tan(self.helix_angle) ** 2)
        self.total_inlet_area = pi / 4.0 * self.Dt ** 2
        self.total_volume = self.total_inlet_area * self.tube_length
        if Di is not None:
            self.Di = Di
            self.inner_surface_area = self.tube_length * pi * self.Di
            self.inlet_area = pi / 4.0 * self.Di ** 2
            self.inner_volume = self.inlet_area * self.tube_length
            self.annulus_area = self.total_inlet_area - self.inlet_area
            self.annulus_volume = self.total_volume - self.inner_volume