class RelatedManager:
    related_object_name = None

    def __init__(self, api, base_manager_class, related_object_name, id):
        self.base_manager = base_manager_class(api)
        self.related_object_name = related_object_name
        self.id = id

    def find_all(self, **kwargs):
        kwargs[self.related_object_name] = self.id
        return self.base_manager.find_all(**kwargs)