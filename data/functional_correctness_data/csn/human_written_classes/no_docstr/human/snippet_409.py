from chemicals.utils import PY37, object_data

class JsonOptEncodable:
    json_version = 1
    "This attribute will be encoded into the produced json blob.\n    It is specific to each object. When backwards incompatible changes are made\n    to an object's structure, be sure to increment this to avoid deserializations\n    producing broken objects."
    obj_references = None
    'If this attribute is not None, instead of inspecting each object for whether it is a json-supported type,\n    only these attribute names are inspected for recursion. These are also the only references\n    subject to deduplication.\n    '
    non_json_attributes = []
    'List of attributes to remove from a dict\n    '

    def _custom_as_json(self, cache):
        pass

    def as_json(self, cache=None, option=0):
        base_serializer = cache is None
        if base_serializer:
            num_to_object = {'pyid_0': None}
            id_to_num_str = {id(self): 'pyid_0'}
            cache = (num_to_object, id_to_num_str)
        else:
            num_to_object, id_to_num_str = cache
        d = object_data(self)
        for attr in self.non_json_attributes:
            try:
                del d[attr]
            except:
                pass
        if option & JSON_DROP_RECALCULABLE:
            try:
                for attr in self.recalculable_attributes:
                    try:
                        del d[attr]
                    except:
                        pass
            except:
                pass
        search_recurse = self.obj_references if self.obj_references is not None else list(d.keys())
        for obj_name in search_recurse:
            try:
                o = d[obj_name]
            except:
                continue
            t = type(o)
            if t in primitive_serialization_types_no_containers:
                continue
            if t is list:
                json_obj_list = []
                for v in o:
                    if id(v) in id_to_num_str:
                        num_str = id_to_num_str[id(v)]
                    else:
                        num = len(id_to_num_str)
                        num_str = f'pyid_{num}'
                        id_to_num_str[id(v)] = num_str
                        num_to_object[num_str] = v.as_json(cache)
                    json_obj_list.append(num_str)
                d[obj_name] = json_obj_list
            elif t is dict:
                json_obj_dict = {}
                for k, v in o.items():
                    if id(v) in id_to_num_str:
                        num_str = id_to_num_str[id(v)]
                    else:
                        num = len(id_to_num_str)
                        num_str = f'pyid_{num}'
                        id_to_num_str[id(v)] = num_str
                        num_to_object[num_str] = v.as_json(cache)
                    json_obj_dict[k] = num_str
                d[obj_name] = json_obj_dict
            else:
                if id(o) in id_to_num_str:
                    num_str = id_to_num_str[id(o)]
                else:
                    num = len(id_to_num_str)
                    num_str = f'pyid_{num}'
                    id_to_num_str[id(o)] = num_str
                    num_to_object[num_str] = o.as_json(cache)
                d[obj_name] = num_str
        if self.vectorized:
            d = arrays_to_lists(d)
        d['py/object'] = self.__full_path__
        d['json_version'] = self.json_version
        if hasattr(self, '_custom_as_json'):
            self._custom_as_json(d, cache)
        if base_serializer:
            num_to_object['pyid_0'] = d
            return num_to_object
        return d

    @classmethod
    def from_json(cls, json_repr, cache=None, ref_name='pyid_0'):
        if cache is None:
            cache = {}
        d = json_repr[ref_name]
        num_to_object = json_repr
        class_name = d['py/object']
        json_version = d['json_version']
        del d['py/object']
        del d['json_version']
        original_obj = object_lookups[class_name]
        try:
            new = original_obj.__new__(original_obj)
            cache[ref_name] = new
        except:
            new = original_obj.from_json(d)
            cache[ref_name] = new
            return new
        search_recurse = new.obj_references if new.obj_references is not None else list(d.keys())
        if d.get('vectorized'):
            d = naive_lists_to_arrays(d)
        for obj_name in search_recurse:
            try:
                o = d[obj_name]
            except:
                continue
            t = type(o)
            if t is str and o.startswith('pyid_'):
                if o not in cache:
                    JsonOptEncodable.from_json(json_repr, cache, ref_name=o)
                d[obj_name] = cache[o]
            elif t is list and len(o):
                initial_list_item = o[0]
                if type(initial_list_item) is str and initial_list_item.startswith('pyid_'):
                    created_objs = []
                    for v in o:
                        if v not in cache:
                            JsonOptEncodable.from_json(json_repr, cache, ref_name=v)
                        created_objs.append(cache[v])
                    d[obj_name] = created_objs
            elif t is dict and len(o):
                initial_list_item = next(iter(o.values()))
                if type(initial_list_item) is str and initial_list_item.startswith('pyid_'):
                    created_objs = {}
                    for k, v in o.items():
                        if v not in cache:
                            JsonOptEncodable.from_json(json_repr, cache, ref_name=v)
                        created_objs[k] = cache[v]
                    d[obj_name] = created_objs
        for k, v in d.items():
            setattr(new, k, v)
        if hasattr(new, '_custom_from_json'):
            new._custom_from_json(num_to_object)
        return new