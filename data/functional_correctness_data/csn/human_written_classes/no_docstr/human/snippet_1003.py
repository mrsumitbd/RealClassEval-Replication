from chamber.utils.datastructures import SequenceChoicesEnumMixin, SubstatesChoicesNumEnum
from django.core.exceptions import ValidationError
from django.utils.translation import gettext

class EnumSequenceFieldMixin:

    def __init__(self, *args, **kwargs):
        self.enum = kwargs.pop('enum', None)
        self.prev_field_name = kwargs.pop('prev_field', None)
        assert self.enum is None or isinstance(self.enum, SequenceChoicesEnumMixin)
        if self.enum:
            kwargs['choices'] = self.enum.choices
        super().__init__(*args, **kwargs)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if self.enum:
            prev_value = model_instance.initial_values[self.attname] if model_instance.is_changing else None
            allowed_next_values = self.enum.get_allowed_next_states(prev_value, model_instance)
            if (self.name in model_instance.changed_fields or model_instance.is_adding) and value not in allowed_next_values:
                raise ValidationError(gettext('Allowed choices are {}.').format(', '.join(('{} ({})'.format(*(self.enum.get_label(val), val)) for val in allowed_next_values))))