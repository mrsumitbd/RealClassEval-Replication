
class BasePermission:
    """
    Base class for permission checks.
    """

    def has_permission(self, request, view):
        """
        Checks if the request has the required permission.

        Args:
            request (object): The incoming request.
            view (object): The view being accessed.

        Returns:
            bool: True if the request has permission, False otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Checks if the request has the required permission for the given object.

        Args:
            request (object): The incoming request.
            view (object): The view being accessed.
            obj (object): The object being accessed.

        Returns:
            bool: True if the request has permission, False otherwise.
        """
        return True
