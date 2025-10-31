from typing import Dict, Any, Optional, List, Tuple
from services.config_service import config_service
import random

class ImageConfig:
    """图像配置类"""

    def __init__(self, prompt: str=None, image_size: str=None, batch_size: int=None, num_inference_steps: int=None, guidance_scale: float=None, negative_prompt: str=None, seed: int=None):
        """
        初始化图像配置

        Args:
            prompt: 图像提示词
            image_size: 图像尺寸
            batch_size: 生成数量
            num_inference_steps: 推理步数
            guidance_scale: 引导比例
            negative_prompt: 负面提示词
            seed: 随机种子
        """
        default_config = config_service.get_image_config()
        self.model = default_config['model']
        self.prompt = prompt or config_service.get_random_image_prompt()
        self.image_size = image_size or default_config['image_size']
        self.batch_size = batch_size or default_config['batch_size']
        self.num_inference_steps = num_inference_steps or default_config['num_inference_steps']
        self.guidance_scale = guidance_scale or default_config['guidance_scale']
        self.negative_prompt = negative_prompt or config_service.get_image_config().get('negative_prompt', '')
        self.seed = seed or random.randint(0, 9999999999)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {'model': self.model, 'prompt': self.prompt, 'image_size': self.image_size, 'batch_size': self.batch_size, 'num_inference_steps': self.num_inference_steps, 'guidance_scale': self.guidance_scale, 'negative_prompt': self.negative_prompt, 'seed': self.seed}