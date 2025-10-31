from bezier.hazmat import curve_helpers
import numpy as np

class NewtonSimpleRoot:
    """Callable object that facilitates Newton's method.

    This is meant to be used to compute the Newton update via:

    .. math::

       DF(s, t) \\left[\\begin{array}{c}
           \\Delta s \\\\ \\Delta t \\end{array}\\right] = -F(s, t).

    Args:
        nodes1 (numpy.ndarray): Control points of the first curve.
        first_deriv1 (numpy.ndarray): Control points of the curve
            :math:`B_1'(s)`.
        nodes2 (numpy.ndarray): Control points of the second curve.
        first_deriv2 (numpy.ndarray): Control points of the curve
            :math:`B_2'(t)`.
    """

    def __init__(self, nodes1, first_deriv1, nodes2, first_deriv2):
        self.nodes1 = nodes1
        self.first_deriv1 = first_deriv1
        self.nodes2 = nodes2
        self.first_deriv2 = first_deriv2

    def __call__(self, s, t):
        """This computes :math:`F = B_1(s) - B_2(t)` and :math:`DF(s, t)`.

        .. note::

           There is **almost** identical code in :func:`.newton_refine`, but
           that code can avoid computing the ``first_deriv1`` and
           ``first_deriv2`` nodes in cases that :math:`F(s, t) = 0` whereas
           this function assumes they have been given.

        In the case that :math:`DF(s, t)` is singular, the assumption is that
        the intersection has a multiplicity higher than one (i.e. the root is
        non-simple). **Near** a simple root, it must be the case that
        :math:`DF(s, t)` has non-zero determinant, so due to continuity, we
        assume the Jacobian will be invertible nearby.

        Args:
            s (float): The parameter where we'll compute :math:`B_1(s)` and
                :math:`DF(s, t)`.
            t (float): The parameter where we'll compute :math:`B_2(t)` and
                :math:`DF(s, t)`.

        Returns:
            Tuple[Optional[numpy.ndarray], numpy.ndarray]: Pair of

            * The LHS matrix ``DF``, a ``2 x 2`` array. If ``F == 0`` then
              this matrix won't be computed and :data:`None` will be returned.
            * The RHS vector ``F``, a ``2 x 1`` array.
        """
        s_vals = np.asfortranarray([s])
        b1_s = curve_helpers.evaluate_multi(self.nodes1, s_vals)
        t_vals = np.asfortranarray([t])
        b2_t = curve_helpers.evaluate_multi(self.nodes2, t_vals)
        func_val = b1_s - b2_t
        if np.all(func_val == 0.0):
            return (None, func_val)
        else:
            jacobian = np.empty((2, 2), order='F')
            jacobian[:, :1] = curve_helpers.evaluate_multi(self.first_deriv1, s_vals)
            jacobian[:, 1:] = -curve_helpers.evaluate_multi(self.first_deriv2, t_vals)
            return (jacobian, func_val)