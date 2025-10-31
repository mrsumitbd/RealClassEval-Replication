
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
            },
            "optional": {
                "adapter_path": ("STRING", {"default": "path/to/ip_adapter"}),
            }
        }

    def load(self, model, adapter_path="path/to/ip_adapter"):
        from transformers import pipeline

        ip_adapter = pipeline("image-to-image", model=adapter_path)
        model.ip_adapter = ip_adapter
        return model, ip_adapter
