
class ReadOnlyResourceMixin:

    @staticmethod
    def create(params, args, data):
        raise NotImplementedError("Cannot create on a read-only resource.")

    @staticmethod
    def update(params, args, data):
        raise NotImplementedError("Cannot update on a read-only resource.")

    @staticmethod
    def delete(params, args, data):
        raise NotImplementedError("Cannot delete on a read-only resource.")
