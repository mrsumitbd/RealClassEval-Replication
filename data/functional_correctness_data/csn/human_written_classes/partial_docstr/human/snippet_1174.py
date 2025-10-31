class ViewSetMixin:
    """
    Overrides ``.as_view()`` so that it takes an ``actions_map`` keyword that performs
    the binding of HTTP methods to actions on the view.

    For example, to create a concrete view binding the 'GET' and 'POST' methods
    to the 'list' and 'create' actions...

    view = MyViewSet.as_view({'get': 'list', 'post': 'create'})
    """

    @classmethod
    def as_view(cls, action_map=None, **initkwargs):
        """
        Allows custom request to method routing based on given ``action_map`` kwarg.
        """
        if not action_map:
            raise TypeError('action_map is a required argument.')

        def view(request):
            self = cls(**initkwargs)
            self.request = request
            self.lookup_url_kwargs = self.request.matchdict
            self.action_map = action_map
            self.action = self.action_map.get(self.request.method.lower())
            for method, action in action_map.items():
                handler = getattr(self, action)
                setattr(self, method, handler)
            return self.dispatch(self.request, **self.request.matchdict)
        return view