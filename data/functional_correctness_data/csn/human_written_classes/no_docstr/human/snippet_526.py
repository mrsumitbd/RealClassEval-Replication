class MockOptions:

    def __init__(self, object_name, *field_names):
        self.load_fields(*field_names)
        self.get_latest_by = None
        self.object_name = object_name
        self.model_name = object_name.lower()

    @property
    def label(self):
        return self.object_name

    @property
    def label_lower(self):
        return self.model_name

    def load_fields(self, *field_names):
        fields = {name: MockField(name) for name in field_names}
        for key in ('_forward_fields_map', 'parents', 'fields_map'):
            self.__dict__[key] = {}
            if key == '_forward_fields_map':
                for name, obj in fields.items():
                    self.__dict__[key][name] = obj
        for key in ('local_concrete_fields', 'concrete_fields', 'fields'):
            self.__dict__[key] = []
            for name, obj in fields.items():
                self.__dict__[key].append(obj)