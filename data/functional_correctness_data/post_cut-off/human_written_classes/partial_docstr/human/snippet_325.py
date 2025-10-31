from diffsynth_engine.models.flux import FluxRedux, FluxIPAdapter
from diffsynth_engine.pipelines.flux_image import FluxImagePipeline
from PIL import Image
from diffsynth_engine.utils.download import fetch_model
import torch
from typing import Dict, List, Tuple, Optional
from diffsynth_engine.configs import FluxPipelineConfig, FluxStateDicts, ControlNetParams

class FluxIPAdapterRefTool:
    """
    Use this tool to generate images with reference image based IP-Adapter
    """

    def __init__(self, flux_model_path: str, lora_list: List[Tuple[str, float]]=[], device: str='cuda:0', dtype: torch.dtype=torch.bfloat16, offload_mode: Optional[str]=None):
        config = FluxPipelineConfig(model_path=flux_model_path, model_dtype=dtype, device=device, offload_mode=offload_mode)
        self.pipe: FluxImagePipeline = FluxImagePipeline.from_pretrained(config)
        self.pipe.load_loras(lora_list)
        ip_adapter_path = fetch_model('muse/FLUX.1-dev-IP-Adapter', path='ip-adapter.safetensors', revision='v1')
        ip_adapter: FluxIPAdapter = FluxIPAdapter.from_pretrained(ip_adapter_path, device=device)
        self.pipe.load_ip_adapter(ip_adapter)

    def __call__(self, ref_image: Image.Image, prompt: str, negative_prompt: str='', ref_scale: float=0.8, seed: int=42, num_inference_steps: int=20, controlnet_params: List[ControlNetParams]=[]):
        self.pipe.ip_adapter.set_scale(ref_scale)
        return self.pipe(ref_image=ref_image, prompt=prompt, negative_prompt=negative_prompt, seed=seed, num_inference_steps=num_inference_steps, controlnet_params=controlnet_params)