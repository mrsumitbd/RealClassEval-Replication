
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
                "model": (
                    "Nunchaku Model",
                    {
                        "tooltip": "The Nunchaku model to which the IP-Adapter will be attached. "
                                   "It should be loaded with NunchakuFluxDiTLoader."
                    }
                )
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
        # Import here to avoid unnecessary dependencies if not used
        try:
            from nunchaku.pipelines.ip_adapter import load_ip_adapter_pipeline
        except ImportError:
            raise ImportError(
                "nunchaku.pipelines.ip_adapter is required to load the IP-Adapter pipeline.")

        # Load the IP-Adapter pipeline (downloads from Hugging Face if needed)
        ip_adapter_pipeline = load_ip_adapter_pipeline(model)
        return (model, ip_adapter_pipeline)
