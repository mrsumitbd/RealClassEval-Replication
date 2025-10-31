from textx.scoping import Postponed

class ExtRelativeName:
    """
    Similar as RelativeName.
    Here you specify separately
    - how to find the class.
    - how to find the methods (starting from a class).
    - how to find inherited/chained classes (starting from a class).
    """

    def __init__(self, path_to_definition_object, path_to_target, path_to_extension):
        self.path_to_definition_object = path_to_definition_object
        self.path_to_target = path_to_target
        self.path_to_extension = path_to_extension
        self.postponed_counter = 0

    def get_reference_propositions(self, obj, attr, name_part):
        """
        retrieve a list of reference propositions.
        Args:
            obj: parent
            attr: attribute
            name_part: The name is used to build the list
                (e.g. using a substring-like logic).
        Returns:
            the list of objects representing the proposed references
        """
        from textx import textx_isinstance
        from textx.scoping.tools import get_list_of_concatenated_objects, resolve_model_path
        def_obj = resolve_model_path(obj, self.path_to_definition_object)
        def_objs = get_list_of_concatenated_objects(def_obj, self.path_to_extension)
        obj_list = []
        for def_obj in def_objs:
            if type(def_obj) is Postponed:
                self.postponed_counter += 1
                return def_obj
            tmp_list = resolve_model_path(def_obj, self.path_to_target)
            assert tmp_list is not None
            if not isinstance(tmp_list, list):
                from textx.exceptions import TextXError
                raise TextXError(f'expected path to list in the model ({self.path_to_target})')
            tmp_list = list(filter(lambda x: textx_isinstance(x, attr.cls) and x.name.find(name_part) >= 0, tmp_list))
            obj_list = obj_list + tmp_list
        return list(obj_list)

    def __call__(self, obj, attr, obj_ref):
        lst = self.get_reference_propositions(obj, attr, obj_ref.obj_name)
        if type(lst) is Postponed:
            return lst
        lst = [x for x in lst if x.name == obj_ref.obj_name]
        if len(lst) > 0:
            return lst[0]
        else:
            return None