class SubscriptAndCallable:

    def __init__(self, *args, **kwargs):
        pass

    def __class_getitem__(cls, item):
        return None

    def __call__(self, arg):
        return arg