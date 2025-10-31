
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
        from diffusers.pipelines.nunchaku_ip_adapter import NunchakuIPAdapterPipeline

        clip_model = CLIPVisionModelWithProjection.from_pretrained(
            "huggingface/clip-vit-base-patch32")
        ip_adapter = NunchakuIPAdapterPipeline.from_pretrained(
            "huggingface/nunchaku-ip-adapter", clip_model=clip_model)

        model.ip_adapter = ip_adapter
        return (model, ip_adapter)
