class BaseType:

    def to_dict(self):
        return dict([(k.lstrip('_'), v) for k, v in self.__dict__.items()])

    def to_dict_with_type(self):

        def _dict(obj):
            module = None
            if issubclass(obj.__class__, BaseType):
                data = {}
                for attr, v in obj.__dict__.items():
                    k = attr.lstrip('_')
                    data[k] = _dict(v)
                module = obj.__module__
            elif isinstance(obj, (list, tuple)):
                data = []
                for i, vv in enumerate(obj):
                    data.append(_dict(vv))
            elif isinstance(obj, dict):
                data = {}
                for _k, vv in obj.items():
                    data[_k] = _dict(vv)
            else:
                data = obj
            return {'type': obj.__class__.__name__, 'data': data, 'module': module}
        return _dict(self)