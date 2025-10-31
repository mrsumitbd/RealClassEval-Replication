
class UserContextFormViewMixin:
    """
    Mixin for Django form views that injects a custom context into the form.
    """

    def get_agnocomplete_context(self):
        """
        Return a dictionary of context variables that should be available to the form.
        Override this method to provide custom context data.
        """
        return {}

    def get_form_kwargs(self):
        """
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        """
        kwargs = super().get_form_kwargs()
        kwargs["context"] = self.get_agnocomplete_context()
        return kwargs
