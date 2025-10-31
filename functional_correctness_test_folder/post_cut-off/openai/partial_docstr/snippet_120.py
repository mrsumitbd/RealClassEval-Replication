
import os
import torch
from diffusers import IPAdapterPipeline


class NunchakuIPAdapterLoader:
    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types and tooltips for the node.
        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        """
        return {
            "required": {
                "model": ("MODEL",),
                "ip_adapter_path": ("STRING", {"default": "", "tooltip": "Path to the IP‑Adapter checkpoint"}),
                "ip_adapter_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0,
                                                "tooltip": "Weight of the IP‑Adapter"}),
            },
            "optional": {}
        }

    def load(self, model):
        """
        Load the IP-Adapter pipeline and attach it to the given model.
        Parameters
        ----------
        model : object
            The Nunchaku model to which the IP-Adapter will be attached.
            It should be loaded with :class:`~comfyui_nunchaku.nodes.models.flux.NunchakuFluxDiTLoader`.
        Returns
        -------
        tuple
            The original model and the loaded IP-Adapter pipeline.
        """
        # Retrieve the path from the node inputs (the caller should set it)
        ip_adapter_path = getattr(self, "ip_adapter_path", None)
        if not ip_adapter_path:
            raise ValueError("IP‑Adapter path not provided")

        # Resolve relative paths
        if not os.path.isabs(ip_adapter_path):
            ip_adapter_path = os.path.abspath(ip_adapter_path)

        if not os.path.exists(ip_adapter_path):
            raise FileNotFoundError(
                f"IP‑Adapter checkpoint not found: {ip_adapter_path}")

        # Determine device and dtype from the model if possible
        device = getattr(model, "device", torch.device("cpu"))
        dtype = getattr(model, "dtype", torch.float16)

        # Load the IP‑Adapter pipeline
        ip_adapter = IPAdapterPipeline.from_pretrained(
            ip_adapter_path,
            torch_dtype=dtype,
            device=device
        )

        # Attach the IP‑Adapter to the model
        setattr(model, "ip_adapter", ip_adapter)
        setattr(model, "ip_adapter_weight", getattr(
            self, "ip_adapter_weight", 1.0))

        return (model, ip_adapter)
