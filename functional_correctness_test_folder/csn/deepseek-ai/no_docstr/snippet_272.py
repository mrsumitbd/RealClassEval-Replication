
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        context = super().get_context_data()
        if hasattr(self, 'request'):
            context['user'] = self.request.user
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'request'):
            kwargs['user'] = self.request.user
        return kwargs
