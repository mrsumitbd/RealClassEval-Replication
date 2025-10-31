from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import smart_str

class MultipleObjectMixin:
    allow_empty = True
    context_object_name = None
    model = None
    queryset = None

    def get_queryset(self):
        """Get the list of items for this view.

        This must be an iterable, and may be a queryset
        (in which qs-specific behavior will be enabled).

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            msg = '{0} must define ``queryset`` or ``model``'
            raise ImproperlyConfigured(msg.format(self.__class__.__name__))
        return queryset

    def get_allow_empty(self):
        """Returns True if the view should display empty lists.

        Return False if a 404 should be raised instead.

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """Get the name of the item to be used in the context.

        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.context_object_name:
            return self.context_object_name
        if hasattr(object_list, 'model'):
            object_name = object_list.model._meta.object_name.lower()
            return smart_str(f'{object_name}_list')
        return None

    def get_context_data(self, **kwargs):
        """Get the context for this view.

        Also adds the *page_template* variable in the context.

        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is generated using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.

        For instance, if the list is a queryset of *blog.Entry*,
        the template will be ``blog/entry_list_page.html``.
        """
        queryset = kwargs.pop('object_list')
        page_template = kwargs.pop('page_template')
        context_object_name = self.get_context_object_name(queryset)
        context = {'object_list': queryset, 'view': self}
        context.update(kwargs)
        if context_object_name is not None:
            context[context_object_name] = queryset
        if page_template is None:
            if hasattr(queryset, 'model'):
                page_template = self.get_page_template(**kwargs)
            else:
                raise ImproperlyConfigured('AjaxListView requires a page_template')
        context['page_template'] = self.page_template = page_template
        return context