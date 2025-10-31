import functools
from lewis.core.exceptions import LewisException, LimitViolationException

class check_limits:
    """
    This decorator helps to make sure that the parameter of a property setter (or any other
    method with one argument) is within certain numerical limits.

    It's possible to set static limits using floats or ints:

    .. sourcecode:: Python

        class Foo:
            _bar = 0

            @property
            def bar(self):
                return self._bar

            @bar.setter
            @check_limits(0, 15)
            def bar(self, new_value):
                self._bar = new_value

    But sometimes this is not flexible enough, so it's also possible to supply strings, which
    are the names of attributes of the object the decorated method belongs with:

    .. sourcecode:: Python

        class Foo:
            _bar = 0

            bar_min = 0
            bar_max = 24

            @property
            def bar(self):
                return self._bar

            @bar.setter
            @check_limits("bar_min", "bar_max")
            def bar(self, new_value):
                self._bar = new_value

    This will make sure that the new value is always between ``bar_min`` and ``bar_max``, even
    if they change at runtime. If the limit is ``None`` (default), the value will not be limited
    in that direction.

    Upper and lower limit can also be used exclusively, for example for a property that has a lower
    bound but not an upper, say a temperature:

    .. sourcecode:: Python

        class Foo:
            _temp = 273.15

            @check_limits(lower=0)
            def set_temperature(self, t_in_kelvin):
                self._temp = t_in_kelvin


    If the value is outside the specified limits, the decorated function is not called and a
    :class:`~lewis.core.exceptions.LimitViolationException` is raised if the ``silent``-
    parameter is ``False`` (default). If that option is active, the call is simply silently
    ignored.

    :param lower: Numerical lower limit or name of attribute that contains limit.
    :param upper: Numerical upper limit or name of attribute that contains limit.
    :param silent: A limit violation will not raise an exception if this option is ``True``.
    """

    def __init__(self, lower=None, upper=None, silent=False) -> None:
        self._lower = lower
        self._upper = upper
        self._silent = silent

    def __call__(self, f):

        @functools.wraps(f)
        def limit_checked(obj, new_value):
            lower = getattr(obj, self._lower) if isinstance(self._lower, str) else self._lower
            upper = getattr(obj, self._upper) if isinstance(self._upper, str) else self._upper
            if (lower is None or lower <= new_value) and (upper is None or new_value <= upper):
                return f(obj, new_value)
            if not self._silent:
                raise LimitViolationException('%f is outside limits (%r, %r)' % (new_value, lower, upper))
        return limit_checked