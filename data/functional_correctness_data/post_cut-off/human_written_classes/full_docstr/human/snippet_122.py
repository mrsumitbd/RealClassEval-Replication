import comfy.model_patcher
from nunchaku.utils import check_hardware_compatibility, get_gpu_memory, get_precision_from_quantization_config
import folder_paths
import comfy.utils

class NunchakuQwenImageDiTLoader:
    """
    Loader for Nunchaku Qwen-Image models.

    Attributes
    ----------
    RETURN_TYPES : tuple
        Output types for the node ("MODEL",).
    FUNCTION : str
        Name of the function to call ("load_model").
    CATEGORY : str
        Node category ("Nunchaku").
    TITLE : str
        Node title ("Nunchaku Qwen-Image DiT Loader").
    """

    @classmethod
    def INPUT_TYPES(s):
        """
        Define the input types and tooltips for the node.

        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        """
        return {'required': {'model_name': (folder_paths.get_filename_list('diffusion_models'), {'tooltip': 'The Nunchaku Qwen-Image model.'}), 'cpu_offload': (['auto', 'enable', 'disable'], {'default': 'auto', 'tooltip': "Whether to enable CPU offload for the transformer model.auto' will enable it if the GPU memory is less than 15G."})}}
    RETURN_TYPES = ('MODEL',)
    FUNCTION = 'load_model'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku Qwen-Image DiT Loader'

    def load_model(self, model_name: str, cpu_offload: str, **kwargs):
        """
        Load the Qwen-Image model from file and return a patched model.

        Parameters
        ----------
        model_name : str
            The filename of the Qwen-Image model to load.
        cpu_offload : str
            Whether to enable CPU offload for the transformer model.

        Returns
        -------
        tuple
            A tuple containing the loaded and patched model.
        """
        model_path = folder_paths.get_full_path_or_raise('diffusion_models', model_name)
        sd, metadata = comfy.utils.load_torch_file(model_path, return_metadata=True)
        model = load_diffusion_model_state_dict(sd, metadata=metadata)
        if cpu_offload == 'auto':
            if get_gpu_memory() < 15:
                cpu_offload_enabled = True
                logger.info('VRAM < 15GiB, enabling CPU offload')
            else:
                cpu_offload_enabled = False
                logger.info('VRAM > 15GiB, disabling CPU offload')
        elif cpu_offload == 'enable':
            cpu_offload_enabled = True
            logger.info('Enabling CPU offload')
        else:
            assert cpu_offload == 'disable', 'Invalid CPU offload option'
            cpu_offload_enabled = False
            logger.info('Disabling CPU offload')
        if cpu_offload_enabled:
            model.model.diffusion_model.set_offload(cpu_offload_enabled)
        return (model,)