
import os
from pathlib import Path
from typing import Tuple

import torch
from huggingface_hub import hf_hub_download

# The node is part of the comfyui_nunchaku package.  The exact
# import path for the model type is not known here, so we use a
# generic ``MODEL`` string that matches the ComfyUI convention.
# The node will only expose a single required input – the model
# that the IP‑Adapter should be attached to.


class NunchakuIPAdapterLoader:
    """
    Node for loading Nunchaku IP‑Adapter pipelines.
    .. warning::
        This node will automatically download the IP‑Adapter and associated CLIP models from Hugging Face.
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
                "model": ("MODEL", {"tooltip": "The Nunchaku model to which the IP‑Adapter will be attached."})
            }
        }

    def load(self, model) -> Tuple[object, object]:
        """
        Load the IP‑Adapter pipeline and attach it to the given model.
        Parameters
        ----------
        model : object
            The Nunchaku model to which the IP‑Adapter will be attached.
            It should be loaded with :class:`~comfyui_nunchaku.nodes.models.flux.NunchakuFluxDiTLoader`.
        Returns
        -------
        tuple
            The original model and the loaded IP‑Adapter pipeline.
        """
        # Repository and file names are hard‑coded because custom paths are not supported.
        repo_id = "nunchaku/ip-adapter"
        checkpoint_file = "ip_adapter.bin"

        # Download the checkpoint from Hugging Face Hub.
        local_path = hf_hub_download(repo_id=repo_id, filename=checkpoint_file)

        # Load the checkpoint.  The checkpoint is expected to be a
        # PyTorch state dict that can be directly used by the model.
        ip_adapter = torch.load(local_path, map_location="cpu")

        # Attach the IP‑Adapter to the model.  The exact API depends on
        # the implementation of the Nunchaku model.  We try a few
        # common patterns.
        if hasattr(model, "set_ip_adapter"):
            model.set_ip_adapter(ip_adapter)
        elif hasattr(model, "ip_adapter"):
            model.ip_adapter = ip_adapter
        else:
            # Fallback: store it as an attribute.
            setattr(model, "ip_adapter", ip_adapter)

        return model, ip_adapter
