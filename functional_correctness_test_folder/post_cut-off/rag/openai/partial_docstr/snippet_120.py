
import os
from typing import Tuple

import torch
from huggingface_hub import hf_hub_download


class NunchakuIPAdapterLoader:
    """
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    """

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
                "model": (
                    "NunchakuFluxDiTLoader",
                    {
                        "tooltip": (
                            "The Nunchaku Flux DiT model to which the IP-Adapter will be attached."
                        ),
                    },
                ),
            },
            "optional": {
                "adapter_repo_id": (
                    "STRING",
                    {
                        "default": "nunchaku/ip-adapter",
                        "tooltip": (
                            "Hugging Face repository ID that hosts the IP-Adapter checkpoint."
                        ),
                    },
                ),
                "adapter_file": (
                    "STRING",
                    {
                        "default": "ip_adapter.bin",
                        "tooltip": (
                            "File name of the IP-Adapter checkpoint inside the repository."
                        ),
                    },
                ),
            },
        }

    def load(self, model) -> Tuple[object, object]:
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
        # Retrieve optional arguments from the node's context if available
        adapter_repo_id = getattr(
            self, "adapter_repo_id", "nunchaku/ip-adapter")
        adapter_file = getattr(self, "adapter_file", "ip_adapter.bin")

        # Download the checkpoint from Hugging Face
        adapter_path = hf_hub_download(
            repo_id=adapter_repo_id,
            filename=adapter_file,
            force_download=False,
        )

        # Load the checkpoint (assumed to be a PyTorch state dict)
        ip_adapter_state = torch.load(adapter_path, map_location="cpu")

        # Attach the IP-Adapter to the model
        # The exact attribute name may vary; we use a generic one.
        setattr(model, "ip_adapter", ip_adapter_state)

        return model, ip_adapter_state
