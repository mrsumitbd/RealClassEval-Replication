from rest_framework_json_api.utils import Hyperlink, get_included_resources, get_resource_type_from_instance, undo_format_link_segment

class PreloadIncludesMixin:
    """
    This mixin provides a helper attributes to select or prefetch related models
    based on the include specified in the URL.

    __all__ can be used to specify a prefetch which should be done regardless of the include


    .. code:: python

        # When MyViewSet is called with ?include=author it will prefetch author and authorbio
        class MyViewSet(viewsets.ModelViewSet):
            queryset = Book.objects.all()
            prefetch_for_includes = {
                '__all__': [],
                'category.section': ['category']
            }
            select_for_includes = {
                '__all__': [],
                'author': ['author', 'author__authorbio'],
            }
    """

    def get_select_related(self, include):
        return getattr(self, 'select_for_includes', {}).get(include, None)

    def get_prefetch_related(self, include):
        return getattr(self, 'prefetch_for_includes', {}).get(include, None)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        included_resources = get_included_resources(self.request, self.get_serializer_class())
        for included in included_resources + ['__all__']:
            select_related = self.get_select_related(included)
            if select_related is not None:
                qs = qs.select_related(*select_related)
            prefetch_related = self.get_prefetch_related(included)
            if prefetch_related is not None:
                qs = qs.prefetch_related(*prefetch_related)
        return qs