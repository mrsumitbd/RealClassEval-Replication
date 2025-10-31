
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        """
        Returns a context dictionary for agnocomplete.
        Override this method to provide custom context.
        """
        return {}

    def get_form_kwargs(self):
        '''
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        '''
        kwargs = {}
        context = self.get_agnocomplete_context()
        if context:
            kwargs['context'] = context
        return kwargs
