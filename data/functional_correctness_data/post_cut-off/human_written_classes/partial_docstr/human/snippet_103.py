import torch
from nunchaku.models.pulid.pulid_forward import pulid_forward
import numpy as np
from types import MethodType
from functools import partial

class NunchakuPulidApply:
    """
    Deprecated node for applying PuLID to a Nunchaku FLUX model.

    Attributes
    ----------
    pulid_device : str
        The device to use for PuLID inference (default: "cuda").
    weight_dtype : torch.dtype
        The data type for model weights (default: torch.bfloat16).
    onnx_provider : str
        The ONNX provider for InsightFace ("gpu" or "cpu", default: "gpu").
    pretrained_model : object or None
        The loaded PuLID model, if any.

    .. warning::
        This node is deprecated and will be removed in December 2025.
        Please use :class:`NunchakuFluxPuLIDApplyV2` instead.
    """

    def __init__(self):
        self.pulid_device = 'cuda'
        self.weight_dtype = torch.bfloat16
        self.onnx_provider = 'gpu'
        self.pretrained_model = None

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types and tooltips for the node.

        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        """
        return {'required': {'pulid': ('PULID', {'tooltip': 'from Nunchaku Pulid Loader'}), 'image': ('IMAGE', {'tooltip': 'The image to encode'}), 'model': ('MODEL', {'tooltip': 'The nunchaku model.'}), 'ip_weight': ('FLOAT', {'default': 1.0, 'min': 0.0, 'max': 2.0, 'step': 0.01, 'tooltip': 'ip_weight'})}}
    RETURN_TYPES = ('MODEL',)
    FUNCTION = 'apply'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku Pulid Apply (Deprecated)'

    def apply(self, pulid, image, model, ip_weight):
        """
        Apply PuLID identity embeddings to the given Nunchaku FLUX model.

        Parameters
        ----------
        pulid : object
            The PuLID pipeline instance.
        image : torch.Tensor
            The image to encode for identity.
        model : object
            The Nunchaku FLUX model.
        ip_weight : float
            The weight for the identity embedding.

        Returns
        -------
        tuple
            The updated model with PuLID applied.
        """
        logger.warning('This node is deprecated and will be removed in December 2025. Directly use "Nunchaku FLUX PuLID Apply V2" instead.')
        image = image.squeeze().cpu().numpy() * 255.0
        image = np.clip(image, 0, 255).astype(np.uint8)
        id_embeddings, _ = pulid.get_id_embedding(image)
        model.model.diffusion_model.model.forward = MethodType(partial(pulid_forward, id_embeddings=id_embeddings, id_weight=ip_weight), model.model.diffusion_model.model)
        return (model,)