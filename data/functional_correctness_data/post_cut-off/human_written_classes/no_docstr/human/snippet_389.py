class ComponentRegistry:

    def __init__(self):
        self.component_dict = {}

    def register(self, cls_name: str, cls):
        if cls_name in self.component_dict:
            raise ValueError(f'Component `{cls_name}` is already registered!')
        self.component_dict[cls_name] = cls

    def get_component(self, cls_name: str):
        if cls_name not in self.component_dict:
            raise KeyError(f'Component `{cls_name}` not found!')
        return self.component_dict[cls_name]

    def has_component(self, cls_name: str) -> bool:
        return cls_name in self.component_dict