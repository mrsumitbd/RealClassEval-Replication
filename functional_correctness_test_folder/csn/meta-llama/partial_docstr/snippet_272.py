
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        """Return the context for agnocomplete."""
        return {'user': self.request.user}

    def get_form_kwargs(self):
        '''
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        '''
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'agnocomplete_context': self.get_agnocomplete_context(),
        })
        return kwargs
