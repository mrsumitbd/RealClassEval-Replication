class Dependency:
    """Non-overriding descriptor for declaring required dependencies in metsrw
    classes. In the following example usage the ``FSEntry`` class is declaring
    a dependency on a feature named 'premis_object_class' which is a class and
    which has methods ``fromtree`` and ``serialize``::

        >>> from .di import is_class, has_methods, Dependency
        >>> class FSEntry(object):
        ...     premis_object_class = Dependency(
        ...         has_methods('serialize'),
        ...         has_class_methods('fromtree'),
        ...         is_class)

    """

    def __init__(self, *assertions):
        self.dependency_name = None
        self.assertions = assertions

    def __get__(self, instance, owner):
        obj = feature_broker[self.dependency_name]
        for assertion in self.assertions:
            assert assertion(obj), f'The value {obj!r} of {self.dependency_name!r} does not match the specified criteria'
        return obj