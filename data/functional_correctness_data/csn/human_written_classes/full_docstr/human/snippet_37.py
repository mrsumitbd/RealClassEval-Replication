class RulesModelMixin:
    """
    A mixin for Django's Model that adds hooks for stepping into the process of
    permission registration, which are called by the metaclass implementation in
    RulesModelBaseMixin.

    Use this mixin in a custom subclass of Model in order to change its behavior.
    """

    @classmethod
    def get_perm(cls, perm_type):
        """Converts permission type ("add") to permission name ("app.add_modelname")

        :param perm_type: "add", "change", etc., or custom value
        :type  perm_type: str
        :returns str:
        """
        return '%s.%s_%s' % (cls._meta.app_label, perm_type, cls._meta.model_name)

    @classmethod
    def preprocess_rules_permissions(cls, perms):
        """May alter a permissions dict before it's processed further.

        Use this, for instance, to alter the supplied permissions or insert default
        values into the given dict.

        :param perms:
            Shallow-copied value of the rules_permissions model Meta option
        :type  perms: dict
        """