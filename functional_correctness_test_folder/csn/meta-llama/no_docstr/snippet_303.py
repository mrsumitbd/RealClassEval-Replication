
class ReadOnlyResourceMixin:

    @staticmethod
    def create(params, args, data):
        raise NotImplementedError(
            "Create operation is not supported for this resource")

    @staticmethod
    def update(params, args, data):
        raise NotImplementedError(
            "Update operation is not supported for this resource")

    @staticmethod
    def delete(params, args, data):
        raise NotImplementedError(
            "Delete operation is not supported for this resource")
