class UserContextFormViewMixin:
    def get_agnocomplete_context(self):
        user = getattr(getattr(self, "request", None), "user", None)
        return {"user": user} if user is not None else {}

    def get_form_kwargs(self):
        '''
        Return the form kwargs.
        This method injects the context variable, defined in
        :meth:`get_agnocomplete_context`. Override this method to adjust it to
        your needs.
        '''
        kwargs = {}
        try:
            kwargs = super().get_form_kwargs()
        except AttributeError:
            pass
        kwargs["agnocomplete_context"] = self.get_agnocomplete_context()
        return kwargs
