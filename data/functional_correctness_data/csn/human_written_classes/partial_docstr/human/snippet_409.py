from textx.scoping import Postponed

class RelativeName:
    """
    allows to implement a class-method-instance-like scoping:
     - define a class with methods
     - define instances
     - allow to define a scope where the instance references the methods
    Note: The same as for classes/methods can be interpreted as
    components/slots...
    """

    def __init__(self, path_to_container_object):
        """
        Here, you specify the path from the instance to the methods:
        The path is given in a dot-separated way: "classref.methods". Then a
        concrete method "f" is searched as "classref.methods.f".

        Args:
            path_to_container_object: This identifies (starting from the
            instance) how to find the methods.
        """
        self.path_to_container_object = path_to_container_object
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
        from textx.scoping.tools import resolve_model_path
        obj_list = resolve_model_path(obj, self.path_to_container_object)
        if type(obj_list) is Postponed:
            self.postponed_counter += 1
            return obj_list
        if not isinstance(obj_list, list):
            from textx.exceptions import TextXError
            raise TextXError(f'expected path to list in the model ({self.path_to_container_object})')
        obj_list = filter(lambda x: textx_isinstance(x, attr.cls) and x.name.find(name_part) >= 0, obj_list)
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