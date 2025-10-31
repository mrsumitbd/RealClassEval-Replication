
class NunchakuIPAdapterLoader:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "ip_adapter_path": ("STRING", {"default": ""}),
                "config_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "device": ("STRING", {"default": "cpu"}),
            }
        }

    def load(self, model):
        import torch
        import os

        ip_adapter_path = getattr(self, "ip_adapter_path", None)
        config_path = getattr(self, "config_path", None)
        device = getattr(self, "device", "cpu")

        if not ip_adapter_path or not os.path.isfile(ip_adapter_path):
            raise FileNotFoundError(
                f"IP Adapter weights not found at {ip_adapter_path}")
        if not config_path or not os.path.isfile(config_path):
            raise FileNotFoundError(f"Config file not found at {config_path}")

        # Dummy loading logic, as actual implementation depends on external libraries
        # Here, we just simulate loading weights and config into the model
        weights = torch.load(ip_adapter_path, map_location=device)
        with open(config_path, "r") as f:
            config = f.read()

        # Simulate attaching weights and config to the model
        model.ip_adapter_weights = weights
        model.ip_adapter_config = config
        model.ip_adapter_device = device

        return model
