import functools
import warnings

class deprecated:
    """A decorator for marking deprecated objects.

    Used internally by SoCo to cause a warning to be issued when the object
    is used, and marks the object as deprecated in the Sphinx documentation.

    Args:
        since (str): The version in which the object is deprecated.
        alternative (str, optional): The name of an alternative object to use
        will_be_removed_in (str, optional): The version in which the object is
            likely to be removed.
        alternative_not_referable (bool): (optional) Indicate that
            ``alternative`` cannot be used as a sphinx reference

    Example:
        ..  code-block:: python

            @deprecated(since="0.7", alternative="new_function")
            def old_function(args):
                pass
    """

    def __init__(self, since, alternative=None, will_be_removed_in=None, alternative_not_referable=False):
        self.since_version = since
        self.alternative = alternative
        self.will_be_removed_in = will_be_removed_in
        self.alternative_not_referable = alternative_not_referable

    def __call__(self, deprecated_fn):

        @functools.wraps(deprecated_fn)
        def decorated(*args, **kwargs):
            message = 'Call to deprecated function {}.'.format(deprecated_fn.__name__)
            if self.will_be_removed_in is not None:
                message += ' Will be removed in version {}.'.format(self.will_be_removed_in)
            if self.alternative is not None:
                message += ' Use {} instead.'.format(self.alternative)
            warnings.warn(message, stacklevel=2)
            return deprecated_fn(*args, **kwargs)
        docs = '\n\n  .. deprecated:: {}\n'.format(self.since_version)
        if self.will_be_removed_in is not None:
            docs += '\n     Will be removed in version {}.'.format(self.will_be_removed_in)
        if self.alternative is not None:
            if self.alternative_not_referable:
                docs += '\n     Use ``{}`` instead.'.format(self.alternative)
            else:
                docs += '\n     Use `{}` instead.'.format(self.alternative)
        if decorated.__doc__ is None:
            decorated.__doc__ = ''
        decorated.__doc__ += docs
        return decorated