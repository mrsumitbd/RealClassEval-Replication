import comfy
import folder_paths

class NunchakuTextEncoderLoaderV2:
    """
    Node for loading Nunchaku text encoders. It also supports 16-bit and FP8 variants.

    .. note::
        When loading our 4-bit T5, a 16-bit T5 is first initialized on a meta device,
        then replaced by the Nunchaku T5.

    .. warning::
        Our 4-bit T5 currently requires a CUDA device.
        If not on CUDA, the model will be moved automatically, which may cause out-of-memory errors.
        Turing GPUs (20-series) are not supported for now.
    """
    RETURN_TYPES = ('CLIP',)
    FUNCTION = 'load_text_encoder'
    CATEGORY = 'Nunchaku'
    TITLE = 'Nunchaku Text Encoder Loader V2'

    @classmethod
    def INPUT_TYPES(s):
        """
        Defines the input types and tooltips for the node.

        Returns
        -------
        dict
            A dictionary specifying the required inputs and their descriptions for the node interface.
        """
        return {'required': {'model_type': (['flux.1'],), 'text_encoder1': (folder_paths.get_filename_list('text_encoders'),), 'text_encoder2': (folder_paths.get_filename_list('text_encoders'),), 't5_min_length': ('INT', {'default': 512, 'min': 256, 'max': 1024, 'step': 128, 'display': 'number', 'lazy': True, 'tooltip': 'Minimum sequence length for the T5 encoder.'})}}

    def load_text_encoder(self, model_type: str, text_encoder1: str, text_encoder2: str, t5_min_length: int):
        """
        Loads the text encoders with the given configuration.

        Parameters
        ----------
        model_type : str
            The type of model to load (e.g., "flux.1").
        text_encoder1 : str
            Filename of the first text encoder checkpoint.
        text_encoder2 : str
            Filename of the second text encoder checkpoint.
        t5_min_length : int
            Minimum sequence length for the T5 encoder.

        Returns
        -------
        tuple
            Tuple containing the loaded CLIP model.
        """
        text_encoder_path1 = folder_paths.get_full_path_or_raise('text_encoders', text_encoder1)
        text_encoder_path2 = folder_paths.get_full_path_or_raise('text_encoders', text_encoder2)
        if model_type == 'flux.1':
            clip_type = comfy.sd.CLIPType.FLUX
        else:
            raise ValueError(f'Unknown type {model_type}')
        clip = load_text_encoder_state_dicts([text_encoder_path1, text_encoder_path2], embedding_directory=folder_paths.get_folder_paths('embeddings'), clip_type=clip_type, model_options={})
        clip.tokenizer.t5xxl.min_length = t5_min_length
        return (clip,)