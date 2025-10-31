class DefaultResetArgv:
    """Provides default 'reset_argv' callable that returns empty list."""

    def __repr__(self):
        return 'DefaultResetArgv'

    def __call__(self, gallery_conf, script_vars):
        """Return empty list."""
        return []