
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        context = super().get_agnocomplete_context()
        context.update({
            'user': self.request.user,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs
