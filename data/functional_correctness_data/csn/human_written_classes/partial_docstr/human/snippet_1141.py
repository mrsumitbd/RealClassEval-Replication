from lewis.core.exceptions import LewisException, LimitViolationException
from typing import NoReturn
import importlib

class FromOptionalDependency:
    """
    This is a utility class for importing classes from a module or
    replacing them with dummy types if the module can not be loaded.

    Assume module 'a' that does:

    .. sourcecode:: Python

        from b import C, D

    and module 'e' which does:

    .. sourcecode:: Python

        from a import F

    where 'b' is a hard to install dependency which is thus optional.
    To still be able to do:

    .. sourcecode:: Python

        import e

    without raising an error, for example for inspection purposes,
    this class can be used as a workaround in module 'a':

    .. sourcecode:: Python

        C, D = FromOptionalDependency("b").do_import("C", "D")

    which is not as pretty as the actual syntax, but at least it
    can be read in a similar way. If the module 'b' can not be imported,
    stub-types are created that are called 'C' and 'D'. Everything depending
    on these types will work until any of those are instantiated - in that
    case an exception is raised.

    The exception can be controlled via the exception-parameter. If it is a
    string, a LewisException is constructed from it. Alternatively it can
    be an instance of an exception-type. If not provided, a LewisException
    with a standard message is constructed. If it is anything else, a RuntimeError
    is raised.

    Essentially, this class helps deferring ImportErrors until anything from
    the module that was attempted to load is actually used.

    :param module: Module from that symbols should be imported.
    :param exception: Text for LewisException or custom exception object.
    """

    def __init__(self, module, exception=None) -> None:
        self._module = module
        if exception is None:
            exception = "The optional dependency '{}' is required for the functionality you tried to use.".format(self._module)
        if isinstance(exception, str):
            exception = LewisException(exception)
        if not isinstance(exception, BaseException):
            raise RuntimeError('The exception parameter has to be either a string or a an instance of an exception type (derived from BaseException).')
        self._exception = exception

    def do_import(self, *names):
        """
        Tries to import names from the module specified on initialization
        of the FromOptionalDependency-object. In case an ImportError occurs,
        the requested names are replaced with stub objects.

        :param names: List of strings that are used as type names.
        :return: Tuple of actual symbols or stub types with provided names. If there is only one
                 element in the tuple, that element is returned.
        """
        try:
            module_object = importlib.import_module(self._module)
            objects = tuple((getattr(module_object, name) for name in names))
        except ImportError:

            def failing_init(obj, *args, **kwargs) -> NoReturn:
                raise self._exception
            objects = tuple((type(name, (object,), {'__init__': failing_init}) for name in names))
        return objects if len(objects) != 1 else objects[0]