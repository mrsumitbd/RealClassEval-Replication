class UserContextFormViewMixin:
    """
    This mixin injects a context variable into the form kwargs.
    """

    def get_agnocomplete_context(self):
        """
        Return the view's current user.
        Override this method to change the value.
        """
        return getattr(self, "request", None).user if hasattr(self, "request") else None

    def get_form_kwargs(self):
        """
        Return the form kwargs, injecting the context variable defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        """
        kwargs = super().get_form_kwargs()
        kwargs["agnocomplete_context"] = self.get_agnocomplete_context()
        return kwargs
