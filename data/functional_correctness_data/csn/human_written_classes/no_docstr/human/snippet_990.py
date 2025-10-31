class InnerFieldTypeMixin:
    __field_type__ = None

    def __init__(self, *args, **kwargs):
        if 'field_type' in kwargs:
            self.__field_type__ = kwargs.pop('field_type')
        super(InnerFieldTypeMixin, self).__init__(*args, **kwargs)

    def get_field_type(self):
        return self.__field_type__ or self.__class__.__field_type__