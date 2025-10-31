class ClientInput:

    def __init__(self, path, input_type, object_store_ref=None):
        self.path = path
        self.input_type = input_type
        self.object_store_ref = object_store_ref

    @property
    def action_source(self):
        return {'path': self.path, 'object_store_ref': self.object_store_ref}