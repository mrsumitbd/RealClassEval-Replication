
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("STRING", {"default": "default_model"})
            }
        }

    def load(self, model):
        # Placeholder for loading logic
        print(f"Loading model: {model}")
        return model
