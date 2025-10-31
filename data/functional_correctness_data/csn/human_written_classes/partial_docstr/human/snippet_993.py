class ConfigStore:
    """
    Class which, given an item, attempts to find the associated config variable.

    All queries are case insensitive. If a lookup cannot find the item,
    ``None`` is returned. The items are looked up in the following order:

        #. user overrides (stored in ``.overrides``)
        #. environment variables
        #. defaults

    """

    def __init__(self):
        """
        Initialise
        """
        self.overrides = {}
        self.config_lookups = [lookup_env, lookup_defaults]

    def __getitem__(self, item):
        item = item.upper()
        if item in self.overrides:
            return self.overrides[item]
        for lookup in self.config_lookups:
            c = lookup(item)
            if c is not None:
                return c

    def __setitem__(self, key, value):
        self.overrides[key.upper()] = value