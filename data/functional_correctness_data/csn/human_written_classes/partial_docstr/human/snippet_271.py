class HealthCheckPluginDirectory:
    """Django health check registry."""

    def __init__(self):
        self._registry = []

    def reset(self):
        """Reset registry state, e.g. for testing purposes."""
        self._registry = []

    def register(self, plugin, **options):
        """Add the given plugin from the registry."""
        self._registry.append((plugin, options))