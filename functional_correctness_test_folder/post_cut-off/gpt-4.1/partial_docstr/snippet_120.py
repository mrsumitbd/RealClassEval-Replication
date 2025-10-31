
class NunchakuIPAdapterLoader:

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
                "model": ("NunchakuFluxDiT", {
                    "tooltip": "The Nunchaku model loaded with NunchakuFluxDiTLoader to attach the IP-Adapter pipeline to."
                }),
            },
            "optional": {},
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
        # Assume the model has a method or attribute to load/attach the IP-Adapter pipeline.
        # This is a placeholder for the actual implementation.
        if hasattr(model, "load_ip_adapter"):
            ip_adapter_pipeline = model.load_ip_adapter()
        elif hasattr(model, "ip_adapter"):
            ip_adapter_pipeline = model.ip_adapter
        else:
            # Simulate loading or attaching the IP-Adapter pipeline
            class DummyIPAdapterPipeline:
                def __init__(self, model):
                    self.model = model
            ip_adapter_pipeline = DummyIPAdapterPipeline(model)
        return (model, ip_adapter_pipeline)
