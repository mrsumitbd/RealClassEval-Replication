from fluids.numerics import cacos, catan, chebval, derivative, ellipe, ellipeinc, ellipkinc, linspace, newton, quad, secant, translate_bound_func
from cmath import sqrt as csqrt
from math import acos, acosh, asin, atan, cos, degrees, isclose, log, log1p, pi, radians, sin, sqrt, tan

class HyperbolicCoolingTower:
    """Class representing the geometry of a hyperbolic cooling tower, as used
    in many industries especially the poewr industry.  All parameters are also
    attributes.

    `H_inlet`, `D_outlet`, and `H_outlet` are always required. Additionally,
    one set of the following parameters is required; `H_support`, `D_support`,
    `n_support`, and `inlet_rounding` are all optional as well.

        * Inlet diameter
        * Inlet diameter and throat diameter
        * Inlet diameter and throat height
        * Inlet diameter, throat diameter, and throat height
        * Base diameter, throat diameter, and throat height

    If the inlet diameter is provided but the throat diameter and/or the throat
    height are missing, two heuristics are used to estimate them (to avoid
    these heuristics simply specify the values):

        * Assume the throat elevation is 2/3 the elevation of the tower.
        * Assume the throat diameter is 63% the diameter of the inlet.

    Parameters
    ----------
    H_inlet : float
        Height of the inlet zone of the cooling tower (also called rain zone),
        [m]
    D_outlet : float
        The inside diameter of the cooling tower outlet (top of the tower; the
        elevation the concrete section ends), [m]
    H_outlet : float
        The height of the cooling tower outlet (top of the tower;the
        elevation the concrete section ends), [m]
    D_inlet : float, optional
        The inside diameter of the cooling tower inlet at the elevation the
        concrete section begins, [m]
    D_base : float, optional
        The diameter of the cooling tower at the very base of the tower (the
        bottom of the inlet zone, at the elevation of the ground), [m]
    D_throat : float, optional
        The diameter of the cooling tower at its minimum section, called its
        throat; where the two hyperbolas meet, [m]
    h_throat : float, optional
        The elevation of the cooling tower's throat (its minimum section; where
        the two hyperbolas meet), [m]
    inlet_rounding : float, optional
        Radius of an optional rounded protrusion from the lip of the cooling
        tower shell base, which curves upwards from the lip (used to reduce
        the dead zone area rather than having a flat lip), [m]
    H_support : float, optional
        The height of each support column, [m]
    D_support : float, optional
        The diameter of each support column, [m]
    n_support : int, optional
        The number of support columns of the cooling tower, [m]

    Attributes
    ----------
    b_lower : float
        The `b` parameter in the hyperbolic equation for the lower section of
        the cooling tower, [m]
    b_upper : float
        The `b` parameter in the hyperbolic equation for the upper section of
        the cooling tower, [m]

    Notes
    -----
    Note there are two hyperbolas in a hyperbolic cooling tower - one under the
    throat and one above it; they are not necessarily the same.

    A hyperbolic cooling tower is not the absolute optimal design, but is is
    close. The optimality is determined by the amount of material required to
    build it while maintaining its rigidity. For thermal design purposes,
    a hyperbolic model covers any minor variation quite well.

    Examples
    --------
    >>> ct = HyperbolicCoolingTower(D_outlet=89.0, H_outlet=200, D_inlet=136.18, H_inlet=14.5)
    >>> ct
    <Hyperbolic cooling tower, inlet diameter=136.18 m, outlet diameter=89 m, inlet height=14.5 m, outlet height=200 m, throat diameter=85.7934 m, throat height=133.333 m, base diameter=146.427 m>
    >>> ct.diameter(5)
    142.84514486126062

    References
    ----------
    .. [1] Chen, W. F., and E. M. Lui, eds. Handbook of Structural Engineering,
       Second Edition. Boca Raton, Fla: CRC Press, 2005.
    .. [2] Ansary, A. M. El, A. A. El Damatty, and A. O. Nassef. Optimum Shape
       and Design of Cooling Towers, 2011.
    """

    def __repr__(self):
        s = '<Hyperbolic cooling tower, inlet diameter=%g m, outlet diameter=%g m, inlet height=%g m, outlet height=%g m, throat diameter=%g m, throat height=%g m, base diameter=%g m>'
        s = s % (self.D_inlet, self.D_outlet, self.H_inlet, self.H_outlet, self.D_throat, self.H_throat, self.D_base)
        return s

    def __init__(self, H_inlet, D_outlet, H_outlet, D_inlet=None, D_base=None, D_throat=None, H_throat=None, H_support=None, D_support=None, n_support=None, inlet_rounding=None):
        self.D_outlet = D_outlet
        self.H_inlet = H_inlet
        self.H_outlet = H_outlet
        if H_throat is None:
            H_throat = 2 / 3.0 * H_outlet
        self.H_throat = H_throat
        if D_throat is None:
            if D_inlet is not None:
                D_throat = 0.63 * D_inlet
            else:
                raise ValueError('Provide either `D_throat`, or `D_inlet` so it may be estimated.')
        self.D_throat = D_throat
        if D_inlet is None and D_base is None:
            raise ValueError('Need `D_inlet` or `D_base`')
        if D_base is not None:
            b = self.D_throat * self.H_throat / sqrt(D_base ** 2 - self.D_throat ** 2)
            D_inlet = 2 * self.D_throat * sqrt((self.H_throat - H_inlet) ** 2 + b ** 2) / (2 * b)
        elif D_inlet is not None:
            b = self.D_throat * (self.H_throat - H_inlet) / sqrt(D_inlet ** 2 - self.D_throat ** 2)
            D_base = 2 * self.D_throat * sqrt(self.H_throat ** 2 + b ** 2) / (2 * b)
        self.D_inlet = D_inlet
        self.D_base = D_base
        self.b_lower = b
        self.b_upper = self.D_throat * (self.H_outlet - self.H_throat) / sqrt(self.D_outlet ** 2 - self.D_throat ** 2)
        self.H_support = H_support
        self.D_support = D_support
        self.n_support = n_support
        self.inlet_rounding = inlet_rounding

    def plot(self, pts=100):
        import matplotlib.pyplot as plt
        Zs = linspace(0, self.H_outlet, pts)
        Rs = [self.diameter(Z) * 0.5 for Z in Zs]
        plt.plot(Zs, Rs)
        plt.plot(Zs, [-v for v in Rs])
        plt.show()

    def diameter(self, H):
        """Calculates cooling tower diameter at a specified height, using
        the formulas for either hyperbola, depending on the height specified.

        .. math::
            D = D_{throat}\\frac{\\sqrt{H^2 + b^2}}{b}

        The value of `H` and `b` used in the above equation is as follows:

            * `H_throat` - H  and `b_lower` if under the throat
            * `H` - `H_throat` and `b_upper`, if above the throat

        Parameters
        ----------
        H : float
            Height at which to calculate the cooling tower diameter, [m]

        Returns
        -------
        D : float
            Diameter of the cooling tower at the specified height, [m]
        """
        if H <= self.H_throat:
            H = self.H_throat - H
            b = self.b_lower
        else:
            H = H - self.H_throat
            b = self.b_upper
        R = self.D_throat * sqrt(H * H + b * b) / (2.0 * b)
        return R * 2.0