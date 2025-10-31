
class ReadOnlyResourceMixin:

    @staticmethod
    def create(params, args, data):
        raise NotImplementedError(
            "Create operation is not allowed for read-only resources.")

    @staticmethod
    def update(params, args, data):
        raise NotImplementedError(
            "Update operation is not allowed for read-only resources.")

    @staticmethod
    def delete(params, args, data):
        raise NotImplementedError(
            "Delete operation is not allowed for read-only resources.")
