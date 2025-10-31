class Metric:

    def __init__(self, display_name=None):
        """
        :param display_name:
        :return:
        """
        self._display_name = display_name

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    def __repr__(self):
        return 'Metric(display_name="{0}")'.format(self._display_name)