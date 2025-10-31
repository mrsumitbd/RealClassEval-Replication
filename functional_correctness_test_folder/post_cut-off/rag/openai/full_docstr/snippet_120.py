
import logging
from typing import Tuple

try:
    from huggingface_hub import hf_hub_download
except Exception:
    hf_hub_download = None  # pragma: no cover

try:
    from transformers import CLIPModel
except Exception:
    CLIPModel = None  # pragma: no cover

try:
    from nunchaku.ip_adapter import IPAdapter
except Exception:
    IPAdapter = None  # pragma: no cover


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
                    "MODEL",
                    {
                        "tooltip": "The Nunchaku model to which the IP-Adapter will be attached."
                    },
                ),
            }
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
        if model is None:
            raise ValueError("The provided model is None.")

        # If the model already has an IP-Adapter attached, skip reloading
        if hasattr(model, "ip_adapter") and model.ip_adapter is not None:
            logging.info(
                "IP-Adapter already attached to the model; skipping reload.")
            return model, model.ip_adapter

        # Load the IP-Adapter pipeline
        if IPAdapter is None:
            raise ImportError(
                "Could not import IPAdapter from nunchaku.ip_adapter.")
        try:
            ip_adapter = IPAdapter
