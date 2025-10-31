class PluginContext:
    """
    Context to pass to plugins for getting extra information
    """

    def __init__(self, config):
        self.__config = config.copy()

    @property
    def config(self):
        """
        config
        """
        return self.__config