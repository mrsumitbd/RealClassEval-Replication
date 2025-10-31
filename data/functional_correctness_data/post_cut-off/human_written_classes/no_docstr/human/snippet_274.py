class FSDPParameterFilter:

    def __init__(self):
        self.model_parameters_storage = set()

    def __call__(self, tensor):
        return tensor.untyped_storage().data_ptr() not in self.model_parameters_storage

    def update_model_parameters(self, model):
        new_storage = set()
        for p in model.parameters():
            new_storage.add(p.data.untyped_storage().data_ptr())
        self.model_parameters_storage = new_storage