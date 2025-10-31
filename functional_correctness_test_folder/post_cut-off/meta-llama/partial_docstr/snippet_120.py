
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ip_adapter": ("IP_ADAPTER", {"tooltip": "The IP-Adapter to load"}),
                "model": ("MODEL", {"tooltip": "The Nunchaku model to attach the IP-Adapter to"})
            }
        }

    def load(self, ip_adapter, model):
        # Assuming the model has a method to load the IP-Adapter pipeline
        ip_adapter_pipeline = ip_adapter.load_pipeline()
        model.attach_ip_adapter(ip_adapter_pipeline)
        return (model, ip_adapter_pipeline)
