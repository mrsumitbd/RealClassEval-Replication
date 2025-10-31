
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
        return True

    def has_object_permission(self, request, view, obj):
        '''
        Checked when a request is for a specific object. Return ``True`` if permission is granted else ``False``.
        :param request: The request sent to the view.
        :param view:  The instance of the view being accessed.
        :param obj: The object being accessed.
        :return: Boolean
        '''
        return True


class AllowAny(BasePermission):
    '''
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    '''

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsAuthenticated(BasePermission):
    '''
    Allows access only to authenticated users.
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAdminUser(BasePermission):
    '''
    Allows access only to admin users.
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthenticatedOrReadOnly(BasePermission):
    '''
    The request is authenticated as a user, or is a read-only request.
    '''

    def has_permission(self, request, view):
        return (
            request.method in ['GET', 'HEAD', 'OPTIONS']
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in ['GET', 'HEAD', 'OPTIONS']
            or request.user and request.user.is_authenticated
        )
