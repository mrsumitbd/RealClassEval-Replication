class _TimeoutsDescriptor:
    """How long the driver should wait for actions to complete before:
    returning an error https://w3c.github.io/webdriver/#timeouts:

    :param timeouts: values in milliseconds for implicit wait, page load and script timeout

    :returns: Values for implicit timeout, pageLoad timeout and script timeout if set (in milliseconds)
    """

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls):
        return obj._caps.get(self.name)

    def __set__(self, obj, value):
        if all((x in ('implicit', 'pageLoad', 'script') for x in value.keys())):
            obj.set_capability(self.name, value)
        else:
            raise ValueError('Timeout keys can only be one of the following: implicit, pageLoad, script')