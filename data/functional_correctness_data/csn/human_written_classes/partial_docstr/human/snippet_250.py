class KeyBitBase:

    def __init__(self, params=None):
        self.params = params

    def get_data(self, params, view_instance, view_method, request, args, kwargs):
        """
        @rtype: dict
        """
        raise NotImplementedError()