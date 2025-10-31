
from typing import Any, Tuple, Dict


class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        '''
        Defines the input types and tooltips for the node.
        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        '''
        return {
            "required": {
                "model": ("MODEL",),
            },
            "optional": {}
        }

    def load(self, model: Any) -> Tuple[Any, Any]:
        '''
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
        '''
        from transformers import pipeline

        # Assuming the IP-Adapter and CLIP models are available on Hugging Face
        ip_adapter = pipeline("image-classification",
                              model="your-ip-adapter-model-name")
        clip_model = pipeline("feature-extraction",
                              model="your-clip-model-name")

        # Attach the IP-Adapter and CLIP models to the Nunchaku model
        model.ip_adapter = ip_adapter
        model.clip_model = clip_model

        return model, ip_adapter
