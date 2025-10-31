class bothmethod:
    """
    'optional @classmethod'.

    A decorator that allows a method to receive either the class
    object (if called on the class) or the instance object
    (if called on the instance) as its first argument.
    """

    def __init__(self, method):
        self.method = method

    def __get__(self, instance, owner):
        if instance is None:
            return self.method.__get__(owner)
        else:
            return self.method.__get__(instance, owner)