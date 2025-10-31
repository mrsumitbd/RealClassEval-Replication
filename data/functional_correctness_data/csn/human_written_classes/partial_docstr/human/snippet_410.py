class RRELBase:

    def __init__(self):
        pass

    def get_next_matches(self, obj, lookup_list, allowed, matched_path, first_element=False):
        """
        This function yields potential matches encountered along the
        requested RREL.

        Implementation detail: This is the base implementation which
        assumes an apply function. Certain RREL classes overwrite this
        method instead of implementing the apply method.

        Args:
            obj: currently visited model object
            lookup_list: reference name to be looked up
            allowed: a callable to "allow" to visit an object
                in order to prevent infinite recursion loops.
                it is called with allowed(obj, lookup_list, RREL-entry).
            first_element: True, if we did not process any
                model element (else False). This is used to
                distinguish RRELs starting at model level (e.g.,
                'packages*.class') or locally (e.g., '.port').
        Returns (yields):
            yields (obj, lookup_list) to indicate possible
            intermediate matches. The returned obj can be
            Postponed.
        """
        if not allowed(obj, lookup_list, self):
            return
        obj, lookup_list, matched_path = self.apply(obj, lookup_list, matched_path, first_element)
        if obj is None:
            return
        elif isinstance(obj, list):
            for iobj in obj:
                if iobj is not None:
                    yield (iobj, lookup_list, matched_path)
        else:
            yield (obj, lookup_list, matched_path)