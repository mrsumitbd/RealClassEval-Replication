
class NunchakuIPAdapterLoader:
    '''
    Node for loading Nunchaku IP-Adapter pipelines.
    .. warning::
        This node will automatically download the IP-Adapter and associated CLIP models from Hugging Face.
        Custom model paths are not supported for now.
    '''
    @classmethod
    def INPUT_TYPES(s):
        '''
        Defines the input types and tooltips for the node.
        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        '''
        return {
            "required": {
                "model": ("MODEL", {"tooltip": "The Nunchaku model to attach the IP-Adapter to."}),
            }
        }

    def load(self, model):
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
        from transformers import CLIPVisionModelWithProjection
        from diffusers.pipelines.stable_diffusion import StableDiffusionPipeline
        from diffusers.models import ImageProjection

        # Load IP-Adapter and CLIP models from Hugging Face
        clip_model = CLIPVisionModelWithProjection.from_pretrained(
            "h94/IP-Adapter", subfolder="models")
        image_projection = ImageProjection.from_pretrained(
            "h94/IP-Adapter", subfolder="models")

        # Attach IP-Adapter to the model
        if hasattr(model, "add_ip_adapter"):
            model.add_ip_adapter(clip_model, image_projection)
        else:
            raise ValueError(
                "The provided model does not support IP-Adapter attachment.")

        return (model, (clip_model, image_projection))
