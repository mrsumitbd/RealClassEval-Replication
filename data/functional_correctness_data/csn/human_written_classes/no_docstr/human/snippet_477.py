class TriggerRegistry:
    _fields = []

    def append(self, field) -> None:
        self._fields.append([field.model._meta.app_label, field.model.__name__])

    def __iter__(self):
        return iter(self._fields)

    def __contains__(self, field) -> bool:
        target = [field.model._meta.app_label, field.model.__name__]
        return target in self._fields