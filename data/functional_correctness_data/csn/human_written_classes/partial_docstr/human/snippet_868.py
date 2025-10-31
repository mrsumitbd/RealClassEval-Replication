class ureg:
    """Unit registry for pint.

    This is a wrapper around the pint unit registry.
    """

    @staticmethod
    def __getattr__(name):
        global _ureg, UNIT_REGISTER_LOADED
        if not UNIT_REGISTER_LOADED:
            _create_unit_registry()
        return getattr(_ureg, name)

    @staticmethod
    def __dir__(*args, **kwargs):
        global _ureg, UNIT_REGISTER_LOADED
        if not UNIT_REGISTER_LOADED:
            _create_unit_registry()
        return dir(_ureg)