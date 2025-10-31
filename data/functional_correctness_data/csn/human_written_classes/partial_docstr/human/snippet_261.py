from modeltranslation.utils import build_localized_fieldname, build_localized_intermediary_model, build_localized_verbose_name, get_language, resolution_order

class TranslatedRelationIdDescriptor:
    """
    A descriptor used for the original '_id' attribute of a translated
    ForeignKey field.
    """

    def __init__(self, field_name: str, fallback_languages: dict[str, tuple[str, ...]] | None) -> None:
        self.field_name = field_name
        self.fallback_languages = fallback_languages

    def __set__(self, instance, value):
        lang = get_language()
        loc_field_name = build_localized_fieldname(self.field_name, lang)
        loc_attname = instance._meta.get_field(loc_field_name).get_attname()
        setattr(instance, loc_attname, value)
        base_attname = instance._meta.get_field(self.field_name).get_attname()
        instance.__dict__[base_attname] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        langs = resolution_order(get_language(), self.fallback_languages)
        for lang in langs:
            loc_field_name = build_localized_fieldname(self.field_name, lang)
            loc_attname = instance._meta.get_field(loc_field_name).get_attname()
            val = getattr(instance, loc_attname, None)
            if val is not None:
                return val
        return None