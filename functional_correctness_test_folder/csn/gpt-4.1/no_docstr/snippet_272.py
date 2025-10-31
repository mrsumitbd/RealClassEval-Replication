
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        context = {}
        if hasattr(self, 'request') and hasattr(self.request, 'user'):
            context['user'] = self.request.user
        return context

    def get_form_kwargs(self):
        kwargs = {}
        if hasattr(super(), 'get_form_kwargs'):
            kwargs = super().get_form_kwargs()
        context = self.get_agnocomplete_context()
        if context:
            kwargs.update(context)
        return kwargs
