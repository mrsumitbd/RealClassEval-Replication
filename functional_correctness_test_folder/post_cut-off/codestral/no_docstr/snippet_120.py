
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
                "ipadapter_file": ("STRING", {"default": ""}),
                "weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "start_at": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                "end_at": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            }
        }

    def load(self, model, ipadapter_file, weight, start_at, end_at):
        from comfy.ip_adapter import IPAdapter
        ip_adapter = IPAdapter(model, ipadapter_file, weight, start_at, end_at)
        return (ip_adapter,)
