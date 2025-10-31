
class NiceRepr:
    '''
    Inherit from this class and define ``__nice__`` to "nicely" print your
    objects.
    Defines ``__str__`` and ``__repr__`` in terms of ``__nice__`` function
    Classes that inherit from :class:`NiceRepr` should redefine ``__nice__``.
    If the inheriting class has a ``__len__``, method then the default
    ``__nice__`` method will return its length.
    Example:
        >>> import ubelt as ub
        >>> class Foo(ub.NiceRepr):
        ...    def __nice__(self):
        ...        return 'info'
        >>> foo = Foo()
        >>> assert str(foo) == '<Foo(info)>'
        >>> assert repr(foo).startswith('<Foo(info) at ')
    Example:
        >>> import ubelt as ub
        >>> class Bar(ub.NiceRepr):
        ...    pass
        >>> bar = Bar()
        >>> import pytest
        >>> with pytest.warns(RuntimeWarning) as record:
        >>>     assert 'object at' in str(bar)
        >>>     assert 'object at' in repr(bar)
    Example:
        >>> import ubelt as ub
        >>> class Baz(ub.NiceRepr):
        ...    def __len__(self):
        ...        return 5
        >>> baz = Baz()
        >>> assert str(baz) == '<Baz(5)>'
    Example:
        >>> import ubelt as ub
        >>> # If your nice message has a bug, it shouldn't bring down the house
        >>> class Foo(ub.NiceRepr):
        ...    def __nice__(self):
        ...        assert False
        >>> foo = Foo()
        >>> import pytest
        >>> with pytest.warns(RuntimeWarning) as record:
        >>>     print('foo = {!r}'.format(foo))
        foo = <...Foo ...>
    Example:
        >>> import ubelt as ub
        >>> class Animal(ub.NiceRepr):
        ...    def __init__(self):
        ...        ...
        ...    def __nice__(self):
        ...        return ''
        >>> class Cat(Animal):
        >>>     ...
        >>> class Dog(Animal):
        >>>     ...
        >>> class Beagle(Dog):
        >>>     ...
        >>> class Ragdoll(Cat):
        >>>     ...
        >>> instances = [Animal(), Cat(), Dog(), Beagle(), Ragdoll()]
        >>> for inst in instances:
        >>>     print(str(inst))
        <Animal()>
        <Cat()>
        <Dog()>
        <Beagle()>
        <Ragdoll()>
    In the case where you cant or dont want to use ubelt.NiceRepr you can get
    similar behavior by pasting the methods from the following snippet into
    your class:
    .. code:: python
        class MyClass:
            def __nice__(self):
                return 'your concise information'
            def __repr__(self):
                nice = self.__nice__()
                classname = self.__class__.__name__
                return '<{0}({1}) at {2}>'.format(classname, nice, hex(id(self)))
            def __str__(self):
                classname = self.__class__.__name__
                nice = self.__nice__()
                return '<{0}({1})>'.format(classname, nice)
    '''

    def __nice__(self):
        try:
            if hasattr(self, '__len__'):
                return str(len(self))
            else:
                raise NotImplementedError('subclass should override __nice__')
        except Exception as ex:
            import warnings
            warnings.warn(str(ex), category=RuntimeWarning)
            return 'object at {}'.format(hex(id(self)))

    def __repr__(self):
        try:
            nice = self.__nice__()
            classname = self.__class__.__name__
            return '<{0}({1}) at {2}>'.format(classname, nice, hex(id(self)))
        except Exception as ex:
            import warnings
            warnings.warn(str(ex), category=RuntimeWarning)
            return object.__repr__(self)

    def __str__(self):
        try:
            classname = self.__class__.__name__
            nice = self.__nice__()
            return '<{0}({1})>'.format(classname, nice)
        except Exception as ex:
            import warnings
            warnings.warn(str(ex), category=RuntimeWarning)
            return object.__repr__(self)
