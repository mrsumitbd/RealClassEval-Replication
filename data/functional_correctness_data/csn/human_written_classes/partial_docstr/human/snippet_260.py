from modeltranslation.utils import build_localized_fieldname, build_localized_intermediary_model, build_localized_verbose_name, get_language, resolution_order

class TranslatedManyToManyDescriptor:
    """
    A descriptor used to return correct related manager without language fallbacks.
    """

    def __init__(self, field_name: str, fallback_languages: dict[str, tuple[str, ...]] | None) -> None:
        self.field_name = field_name
        self.fallback_languages = fallback_languages

    def __get__(self, instance, owner):
        loc_field_name = build_localized_fieldname(self.field_name, get_language())
        loc_attname = (instance or owner)._meta.get_field(loc_field_name).get_attname()
        return getattr(instance or owner, loc_attname)

    def __set__(self, instance, value):
        loc_field_name = build_localized_fieldname(self.field_name, get_language())
        loc_attname = instance._meta.get_field(loc_field_name).get_attname()
        setattr(instance, loc_attname, value)