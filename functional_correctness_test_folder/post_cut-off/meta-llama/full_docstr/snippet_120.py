
import comfy.sd
from comfy.model_patcher import ModelPatcher


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
                "model": ("MODEL",),
            }
        }

    RETURN_TYPES = ("MODEL", "IPADAPTER")
    RETURN_NAMES = ("model", "ip_adapter")
    FUNCTION = "load"
    CATEGORY = "Nunchaku"

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
        ip_adapter = comfy.sd.load_ip_adapter("models/ip-adapter/sd15")
        ip_adapter.set_model_patcher(ModelPatcher(model))
        return (model, ip_adapter)
