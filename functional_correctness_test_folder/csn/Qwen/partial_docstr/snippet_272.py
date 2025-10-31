
class UserContextFormViewMixin:

    def get_agnocomplete_context(self):
        return {}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.get_agnocomplete_context())
        return kwargs
