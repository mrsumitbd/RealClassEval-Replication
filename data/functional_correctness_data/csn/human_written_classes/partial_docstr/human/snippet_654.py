from bezier.hazmat import curve_helpers
from bezier.hazmat import helpers as _py_helpers
import numpy as np

class NewtonDoubleRoot:
    """Callable object that facilitates Newton's method for double roots.

    This is an augmented version of :class:`NewtonSimpleRoot`.

    For non-simple intersections (i.e. multiplicity greater than 1),
    the curves will be tangent, which forces :math:`B_1'(s) \\times B_2'(t)`
    to be zero. Unfortunately, that quantity is also equal to the
    determinant of the Jacobian, so :math:`DF` will not be full rank.

    In order to produce a system that **can** be solved, an
    an augmented function is computed:

    .. math::

        G(s, t) = \\left[\\begin{array}{c}
            F(s, t) \\\\ \\hline
            B_1'(s) \\times B_2'(t)
            \\end{array}\\right]

    The use of :math:`B_1'(s) \\times B_2'(t)` (with lowered degree in
    :math:`s` and :math:`t`) means that the rank deficiency in
    :math:`DF` can be fixed in:

    .. math::

        DG(s, t) = \\left[\\begin{array}{c | c}
            B_1'(s) & -B_2'(t) \\\\ \\hline
            B_1''(s) \\times B_2'(t) & B_1'(s) \\times B_2''(t)
            \\end{array}\\right]

    (This may not always be full rank, but in the double root / multiplicity
    2 case it will be full rank near a solution.)

    Rather than finding a least squares solution to the overdetermined system

    .. math::

       DG(s, t) \\left[\\begin{array}{c}
           \\Delta s \\\\ \\Delta t \\end{array}\\right] = -G(s, t)

    we find a solution to the square (and hopefully full rank) system:

    .. math::

       DG^T DG \\left[\\begin{array}{c}
           \\Delta s \\\\ \\Delta t \\end{array}\\right] = -DG^T G.

    Forming :math:`DG^T DG` squares the condition number, so it would be
    "better" to use :func:`~numpy.linalg.lstsq` (which wraps the LAPACK routine
    ``dgelsd``). However, using :func:`.solve2x2` is **much** more
    straightforward and in practice this is just as accurate.

    Args:
        nodes1 (numpy.ndarray): Control points of the first curve.
        first_deriv1 (numpy.ndarray): Control points of the curve
            :math:`B_1'(s)`.
        second_deriv1 (numpy.ndarray): Control points of the curve
            :math:`B_1''(s)`.
        nodes2 (numpy.ndarray): Control points of the second curve.
        first_deriv2 (numpy.ndarray): Control points of the curve
            :math:`B_2'(t)`.
        second_deriv2 (numpy.ndarray): Control points of the curve
            :math:`B_2''(t)`.
    """

    def __init__(self, nodes1, first_deriv1, second_deriv1, nodes2, first_deriv2, second_deriv2):
        self.nodes1 = nodes1
        self.first_deriv1 = first_deriv1
        self.second_deriv1 = second_deriv1
        self.nodes2 = nodes2
        self.first_deriv2 = first_deriv2
        self.second_deriv2 = second_deriv2

    def __call__(self, s, t):
        """This computes :math:`DG^T G` and :math:`DG^T DG`.

        If :math:`DG^T DG` is not full rank, this means either :math:`DG`
        was not full rank or that it was, but with a relatively high condition
        number. So, in the case that :math:`DG^T DG` is singular, the
        assumption is that the intersection has a multiplicity higher than two.

        Args:
            s (float): The parameter where we'll compute :math:`G(s, t)` and
                :math:`DG(s, t)`.
            t (float): The parameter where we'll compute :math:`G(s, t)` and
                :math:`DG(s, t)`.

        Returns:
            Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray]]: Pair of

            * The LHS matrix ``DG^T DG``, a ``2 x 2`` array. If ``G == 0`` then
              this matrix won't be computed and :data:`None` will be returned.
            * The RHS vector ``DG^T G``, a ``2 x 1`` array.
        """
        s_vals = np.asfortranarray([s])
        b1_s = curve_helpers.evaluate_multi(self.nodes1, s_vals)
        b1_ds = curve_helpers.evaluate_multi(self.first_deriv1, s_vals)
        t_vals = np.asfortranarray([t])
        b2_t = curve_helpers.evaluate_multi(self.nodes2, t_vals)
        b2_dt = curve_helpers.evaluate_multi(self.first_deriv2, t_vals)
        func_val = np.empty((3, 1), order='F')
        func_val[:2, :] = b1_s - b2_t
        func_val[2, :] = _py_helpers.cross_product(b1_ds[:, 0], b2_dt[:, 0])
        if np.all(func_val == 0.0):
            return (None, func_val[:2, :])
        else:
            jacobian = np.empty((3, 2), order='F')
            jacobian[:2, :1] = b1_ds
            jacobian[:2, 1:] = -b2_dt
            if self.second_deriv1.size == 0:
                jacobian[2, 0] = 0.0
            else:
                jacobian[2, 0] = _py_helpers.cross_product(curve_helpers.evaluate_multi(self.second_deriv1, s_vals)[:, 0], b2_dt[:, 0])
            if self.second_deriv2.size == 0:
                jacobian[2, 1] = 0.0
            else:
                jacobian[2, 1] = _py_helpers.cross_product(b1_ds[:, 0], curve_helpers.evaluate_multi(self.second_deriv2, t_vals)[:, 0])
            modified_lhs = _py_helpers.matrix_product(jacobian.T, jacobian)
            modified_rhs = _py_helpers.matrix_product(jacobian.T, func_val)
            return (modified_lhs, modified_rhs)