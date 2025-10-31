import toolz as tz

class GetRetriever:

    def __init__(self, integrations, samples):
        self._integrations = integrations
        self._samples = samples

    def integration_and_config(self, path):
        """Get a retriever and configuration for the given file path.
        """
        if path.startswith(tuple(INTEGRATION_MAP.keys())):
            key = INTEGRATION_MAP[path.split(':')[0] + ':']
            integration = self._integrations.get(key)
            config = {}
            for sample in self._samples:
                config = tz.get_in(['config', key], sample)
                if config:
                    break
            return (integration, config)
        return (None, None)