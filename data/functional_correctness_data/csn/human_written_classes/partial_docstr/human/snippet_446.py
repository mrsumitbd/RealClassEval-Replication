class Validator:
    """Base class for validators that check and format search command options.

    You must inherit from this class and override :code:`Validator.__call__` and
    :code:`Validator.format`. :code:`Validator.__call__` should convert the
    value it receives as argument and then return it or raise a
    :code:`ValueError`, if the value will not convert.

    :code:`Validator.format` should return a human readable version of the value
    it receives as argument the same way :code:`str` does.

    """

    def __call__(self, value):
        raise NotImplementedError()

    def format(self, value):
        raise NotImplementedError()