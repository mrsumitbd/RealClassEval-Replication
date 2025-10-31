class Method:
    """
    Plugin method.
    @ivar name: The method name.
    @type name: str
    @ivar domain: The plugin domain.
    @type domain: L{PluginDomain}
    """

    def __init__(self, name, domain):
        """
        @param name: The method name.
        @type name: str
        @param domain: A plugin domain.
        @type domain: L{PluginDomain}
        """
        self.name = name
        self.domain = domain

    def __call__(self, **kwargs):
        ctx = self.domain.ctx()
        ctx.__dict__.update(kwargs)
        for plugin in self.domain.plugins:
            try:
                method = getattr(plugin, self.name, None)
                if method and callable(method):
                    method(ctx)
            except Exception as pe:
                log.exception(pe)
        return ctx