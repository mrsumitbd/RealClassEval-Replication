
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "ip_adapter": ("IP_ADAPTER",),
                "weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "start_at": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "end_at": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }

    def load(self, model):
        from comfyui_nunchaku.nodes.ip_adapter import IPAdapterPipeline

        ip_adapter_pipeline = IPAdapterPipeline(model)
        return (model, ip_adapter_pipeline)
