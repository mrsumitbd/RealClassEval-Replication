
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("STRING", {"default": ""}),
            }
        }

    def load(self, model):
        return model
