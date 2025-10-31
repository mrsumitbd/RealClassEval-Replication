class BaseModelIterator:

    def __init__(self, model):
        self.model = model

    def __iter__(self):
        fields = self.model.get_fields()
        for fieldname in fields:
            field = self.model.get_field_obj(fieldname)
            name = self.model.get_real_name(fieldname)
            yield (name, field, self.model.get_field_value(fieldname))