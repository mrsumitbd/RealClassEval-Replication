import torch

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
        return {'required': {'model': ('MODEL', {'tooltip': 'The nunchaku model.'})}}
    RETURN_TYPES = ('MODEL', 'IPADAPTER_PIPELINE')
    FUNCTION = 'load'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku IP-Adapter Loader'

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
        device = model.model.diffusion_model.model.device
        pipeline = IPAFluxPipelineWrapper.from_pretrained('black-forest-labs/FLUX.1-dev', transformer=model.model.diffusion_model.model, torch_dtype=torch.bfloat16).to(device)
        pipeline.load_ip_adapter(pretrained_model_name_or_path_or_dict='XLabs-AI/flux-ip-adapter-v2', weight_name='ip_adapter.safetensors', image_encoder_pretrained_model_name_or_path='openai/clip-vit-large-patch14')
        return (model, pipeline)