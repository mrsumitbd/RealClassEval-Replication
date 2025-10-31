
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "ip_adapter": ("IP_ADAPTER",),
            }
        }

    def load(self, model, ip_adapter):
        # Assuming the actual implementation involves some kind of model and ip_adapter processing
        # For demonstration purposes, it simply returns the model and ip_adapter
        return (model, ip_adapter)
