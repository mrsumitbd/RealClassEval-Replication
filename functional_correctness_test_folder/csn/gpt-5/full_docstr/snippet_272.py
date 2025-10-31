class UserContextFormViewMixin:
    '''
    This mixin is injecting the context variable into the form kwargs
    '''

    def get_agnocomplete_context(self):
        '''
        Return the view current user.
        You may want to change this value by overrding this method.
        '''
        try:
            return self.request.user
        except Exception:
            return None

    def get_form_kwargs(self):
        '''
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        '''
        kwargs = {}
        super_get_form_kwargs = getattr(super(), 'get_form_kwargs', None)
        if callable(super_get_form_kwargs):
            kwargs = super_get_form_kwargs()
        kwargs['agnocomplete_context'] = self.get_agnocomplete_context()
        return kwargs
