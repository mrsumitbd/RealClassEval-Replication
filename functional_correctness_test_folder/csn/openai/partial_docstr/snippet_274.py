class BasePermission:
    '''
    All permission classes should inherit from this class.
    '''

    def has_permission(self, request, view):
        '''
        Checked on every request to a view. Return ``True`` if permission is granted else ``False``.
        :param request: The request sent to the view.
        :param view: The instance of the view being accessed.
        :return: Boolean
        '''
        raise NotImplementedError("Subclasses must implement has_permission")

    def has_object_permission(self, request, view, obj):
        '''
        Checked on requests that involve a specific object. Return ``True`` if permission is granted else ``False``.
        :param request: The request sent to the view.
        :param view: The instance of the view being accessed.
        :param obj: The object being accessed.
        :return: Boolean
        '''
        raise NotImplementedError(
            "Subclasses must implement has_object_permission")
