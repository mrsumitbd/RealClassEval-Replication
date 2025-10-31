class GuardedMixin:
    """Add guarded CRUD methods to resource.

    The ``guard`` replaces the CRUD guarded methods with a wrapper with
    security checks around these methods. It adds this mixin into the
    resource automatically, but it can be declared on the resource manually
    for IDEs to accept calls to the guarded methods.
    """

    def guarded_create(self, params, args, data):
        pass

    def guarded_read(self, params, args, data):
        pass

    def guarded_update(self, params, args, data):
        pass

    def guarded_delete(self, params, args, data):
        pass