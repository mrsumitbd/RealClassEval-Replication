class NestedRouterMixin:

    def _register(self, *args, **kwargs):
        return super().register(*args, **kwargs)

    def register(self, *args, **kwargs):
        self._register(*args, **kwargs)
        return NestedRegistryItem(router=self, parent_prefix=self.registry[-1][0], parent_viewset=self.registry[-1][1])