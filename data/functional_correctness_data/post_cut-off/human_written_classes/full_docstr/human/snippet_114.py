import torch
from nunchaku.pipeline.pipeline_flux_pulid import PuLIDPipeline

class NunchakuPulidLoader:
    """
    Deprecated node for loading the PuLID pipeline for a Nunchaku FLUX model.

    .. warning::
        This node is deprecated and will be removed in December 2025.
        Use :class:`NunchakuPuLIDLoaderV2` instead.

    Attributes
    ----------
    pulid_device : str
        Device to load the PuLID pipeline on (default: "cuda").
    weight_dtype : torch.dtype
        Data type for model weights (default: torch.bfloat16).
    onnx_provider : str
        ONNX provider to use (default: "gpu").
    pretrained_model : str or None
        Path to the pretrained PuLID model, if any.
    """

    def __init__(self):
        """
        Initialize the loader with default device, dtype, and ONNX provider.
        """
        self.pulid_device = 'cuda'
        self.weight_dtype = torch.bfloat16
        self.onnx_provider = 'gpu'
        self.pretrained_model = None

    @classmethod
    def INPUT_TYPES(s):
        """
        Returns the required input types for this node.

        Returns
        -------
        dict
            Dictionary specifying required inputs.
        """
        return {'required': {'model': ('MODEL', {'tooltip': 'The nunchaku model.'})}}
    RETURN_TYPES = ('MODEL', 'PULID')
    FUNCTION = 'load'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku Pulid Loader (Deprecated)'

    def load(self, model):
        """
        Load the PuLID pipeline for the given Nunchaku FLUX model.

        .. warning::
            This node is deprecated and will be removed in December 2025.
            Use :class:`NunchakuPuLIDLoaderV2` instead.

        Parameters
        ----------
        model : object
            The Nunchaku FLUX model.

        Returns
        -------
        tuple
            The input model and the loaded PuLID pipeline.
        """
        logger.warning('This node is deprecated and will be removed in December 2025. Directly use "Nunchaku PuLID Loader V22 instead.')
        pulid_model = PuLIDPipeline(dit=model.model.diffusion_model.model, device=self.pulid_device, weight_dtype=self.weight_dtype, onnx_provider=self.onnx_provider)
        pulid_model.load_pretrain(self.pretrained_model)
        return (model, pulid_model)