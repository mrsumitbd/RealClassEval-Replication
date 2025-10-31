
import os
from pathlib import Path
from typing import Tuple

# Import the Hugging Face hub utilities
try:
    from huggingface_hub import snapshot_download
except ImportError:
    snapshot_download = None  # will raise an error later if used

# Import the IP‑Adapter pipeline from the Nunchaku library
# (the actual import path may differ – adjust if necessary)
try:
    from nunchaku.ip_adapter import IPAdapterPipeline
except ImportError:
    IPAdapterPipeline = None  # will raise an error later if used


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
                "model": ("NunchakuFluxDiT",),
            },
            "optional": {},
            "tooltip": {
                "model": "The Nunchaku Flux DiT model to which the IP‑Adapter will be attached."
            },
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
        # Validate prerequisites
        if snapshot_download is None:
            raise RuntimeError(
                "huggingface_hub is required to download the IP‑Adapter. "
                "Please install it with `pip install huggingface_hub`."
            )
        if IPAdapterPipeline is None:
            raise RuntimeError(
                "nunchaku.ip_adapter.IPAdapterPipeline could not be imported. "
                "Ensure the Nunchaku library is installed and up to date."
            )

        # Define the repository ID for the IP‑Adapter
        repo_id = "nunchaku/ip-adapter"

        # Download the repository to a temporary directory
        local_dir = snapshot_download(repo_id, allow_patterns=[
                                      "*.safetensors", "*.json", "*.pt"])

        # Load the IP‑Adapter pipeline from the downloaded files
        # The pipeline expects a path to the model files
        ip_adapter = IPAdapterPipeline.from_pretrained(local_dir)

        # Attach the IP‑Adapter to the model
        # The exact attribute name may vary; we use a generic one
        setattr(model, "ip_adapter", ip_adapter)

        return model, ip_adapter
