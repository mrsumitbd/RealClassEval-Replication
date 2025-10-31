from module.config import language
from module.base.decorator import del_cached_property

class Resource:
    instances = {}
    cached = []

    def resource_add(self, key):
        Resource.instances[key] = self

    def resource_release(self):
        for cache in self.cached:
            del_cached_property(self, cache)

    @staticmethod
    def parse_property(data, l=None):
        """
        Parse properties of Button or Template object input.
        Such as `area`, `color` and `button`.

        Args:
            data: Dict or str
            l (str): Load from given a language or load from global attribute `language.language`
        """
        if l is None:
            l = language.language
        if isinstance(data, dict):
            return data.get(l)
        else:
            return data