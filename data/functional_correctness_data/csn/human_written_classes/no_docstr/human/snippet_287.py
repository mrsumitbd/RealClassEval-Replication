class PartialUpdateSerializerMixin:

    def save(self, **kwargs):
        self._update_fields = kwargs.get('update_fields', None)
        return super().save(**kwargs)

    def update(self, instance, validated_attrs):
        for attr, value in validated_attrs.items():
            if hasattr(getattr(instance, attr, None), 'set'):
                getattr(instance, attr).set(value)
            else:
                setattr(instance, attr, value)
        if self.partial and isinstance(instance, self.Meta.model):
            instance.save(update_fields=getattr(self, '_update_fields') or get_fields_for_partial_update(opts=self.Meta, init_data=self.get_initial(), fields=self.fields.fields))
        else:
            instance.save()
        return instance