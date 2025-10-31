
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

        # Load the IP-Adapter pipeline from Hugging Face
        ip_adapter_pipeline = pipeline(
            "image-classification", model="your-ip-adapter-model-name")

        # Attach the IP-Adapter pipeline to the model
        model.ip_adapter = ip_adapter_pipeline

        return model, ip_adapter_pipeline
