
class _TaskConfig:
    """
    Simple configuration holder for tasks.

    The configuration is stored internally as a plain dictionary.
    """

    def __init__(self, config=None):
        """
        Create a new configuration instance.

        Parameters
        ----------
        config : dict, optional
            Initial configuration values. If omitted, an empty dictionary is used.
        """
        self._config = dict(config or {})

    def to_dict(self):
        """
        Return a shallow copy of the configuration dictionary.

        Returns
        -------
        dict
            The configuration data.
        """
        return self._config.copy()

    @classmethod
    def from_dict(cls, config):
        """
        Create a new configuration instance from a dictionary.

        Parameters
        ----------
        config : dict
            Configuration data.

        Returns
        -------
        _TaskConfig
            A new configuration instance.
        """
        return cls(config)
