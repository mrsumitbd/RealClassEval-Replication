class EntityAttributesMixin:

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['attrs'] = context['object'].attrs.attributes.values()
        return context

    def form_valid(self, form):
        print('EntityAttributesMixin.form_valid:', self.request.POST)
        return super().form_valid(form)

    def form_invalid(self, form):
        print('EntityAttributesMixin.form_invalid:', self.request.POST)
        return super().form_invalid(form)