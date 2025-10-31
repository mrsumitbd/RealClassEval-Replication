class HostInfoGetter:

    def __init__(self, getter_function, name):
        self.getter_function = getter_function
        self.name = name

    def __call__(self):
        return self.getter_function()

    def get_info(self):
        return self.getter_function()