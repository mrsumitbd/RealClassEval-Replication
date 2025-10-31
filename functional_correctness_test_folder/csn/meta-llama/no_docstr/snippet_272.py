
class UserContextFormViewMixin:
    """
    A mixin that provides a way to pass the user context to a form.
    """

    def get_agnocomplete_context(self):
        """
        Returns the context to be used for agnocomplete.
        """
        return {'user': self.request.user}

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
