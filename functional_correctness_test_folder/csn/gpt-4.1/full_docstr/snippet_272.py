
class UserContextFormViewMixin:
    '''
    This mixin is injecting the context variable into the form kwargs
    '''

    def get_agnocomplete_context(self):
        '''
        Return the view current user.
        You may want to change this value by overrding this method.
        '''
        if hasattr(self, 'request') and hasattr(self.request, 'user'):
            return self.request.user
        return None

    def get_form_kwargs(self):
        '''
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        '''
        kwargs = super().get_form_kwargs() if hasattr(
            super(), 'get_form_kwargs') else {}
        kwargs['context'] = self.get_agnocomplete_context()
        return kwargs
