
class UserContextFormViewMixin:
    """
    Mixin that injects the current user into the form context and form kwargs.
    """

    def get_agnocomplete_context(self):
        """
        Return a dictionary containing the current user.
        This can be used by templates or form widgets that need user‑specific data.
        """
        return {"user": getattr(self, "request", None).user}

    def get_form_kwargs(self):
        """
        Extend the default form kwargs with the current user.
        """
        # Retrieve the base kwargs from the parent class if available
        base_kwargs = {}
        if hasattr(super(), "get_form_kwargs"):
            base_kwargs = super().get_form_kwargs()
        # Inject the user into the kwargs
        base_kwargs.update({"user": getattr(self, "request", None).user})
        return base_kwargs
