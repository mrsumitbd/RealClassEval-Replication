from typing import NoReturn

class CommandBase:
    """
    This is the common base class of :class:`Cmd` and :class:`Var`. The concept of commands for
    the stream adapter is based on connecting a callable object to a pattern that matches an
    inbound request.

    The type of pattern can be either an implementation of :class:`PatternMatcher`
    (regex or scanf format specification) or a plain string (which is treated as a regular
    expression).

    For free function and lambda expressions this is straightforward: the function object can
    simply be stored together with the pattern. Most often however, the callable
    is a method of the device or interface object - these do not exist when the commands are
    defined.

    This problem is solved by introducing a "bind"-step in :class:`StreamAdapter`. So instead
    of a function object, both :class:`Cmd` and :class:`Var` store the name of a member of device
    or interface. At "bind-time", this is translated into the correct callable.

    So instead of using :class:`Cmd` or :class:`Var` directly, both classes' :meth:`bind`-methods
    return an iterable of :class:`Func`-objects which can be used for processing requests.
    :class:`StreamAdapter` performs this bind-step when it's constructed. For details regarding
    the implementations, please see the corresponding classes.

    .. seealso::

        Please take a look at :class:`Cmd` for exposing callable objects or methods of
        device/interface and :class:`Var` for exposing attributes and properties.

        To see how argument_mappings, return_mapping and doc are applied, please look at
        :class:`Func`.

    :param func: Function to be called when pattern matches or member of device/interface.
    :param pattern: Pattern to match (:class:`PatternMatcher` or string).
    :param argument_mappings: Iterable with mapping functions from string to some type.
    :param return_mapping: Mapping function for return value of method.
    :param doc: Description of the command. If not supplied, the docstring is used.
    """

    def __init__(self, func, pattern, argument_mappings=None, return_mapping=None, doc=None) -> None:
        super(CommandBase, self).__init__()
        self.func = func
        self.pattern = pattern
        self.argument_mappings = argument_mappings
        self.return_mapping = return_mapping
        self.doc = doc

    def bind(self, target) -> NoReturn:
        raise NotImplementedError('Binders need to implement the bind method.')