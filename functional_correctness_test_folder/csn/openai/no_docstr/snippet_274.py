
class BasePermission:
    """
    Base class for permission checks. Subclasses should override
    `has_permission` and/or `has_object_permission` to implement
    custom logic.
    """

    def has_permission(self, request, view):
        """
        Return True if the request should be permitted globally.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return True if the request should be permitted for the given object.
        """
        return True
