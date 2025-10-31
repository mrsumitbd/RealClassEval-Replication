class ComponentHandler:
    key = '!'

    def __init__(self, config):
        self.config = config
        self.components = []

    def __call__(self, name, props):
        from .util import resolve_dotted_name
        specification = props.copy()
        factory_dotted_name = specification.pop(self.key)
        factory = resolve_dotted_name(factory_dotted_name)
        component = factory(**specification)
        try:
            component.__pld_config_key__ = name
        except AttributeError:
            pass
        self.components.append(component)
        return component

    def finish(self):
        for component in self.components:
            if hasattr(component, 'initialize_component'):
                component.initialize_component(self.config)