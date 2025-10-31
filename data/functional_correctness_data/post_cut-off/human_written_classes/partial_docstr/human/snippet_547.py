from vllm.utils import STR_DTYPE_TO_TORCH_DTYPE, bind_kv_cache
from vllm.attention import get_attn_backend
import torch
from vllm.platforms import current_platform
from vllm.config import CacheConfig, DeviceConfig, ModelConfig, ParallelConfig, VllmConfig
import torch.distributed
from typing import Dict, List, Optional, Tuple

class RBLNCacheEngine:
    """Manages the KV cache for RBLN backend.

    This class is responsible for initializing and managing RBLN KV
    caches. It also provides methods for performing KV cache operations, such
    as copying.
    """

    def __init__(self, cache_config: CacheConfig, model_config: ModelConfig, parallel_config: ParallelConfig, device_config: DeviceConfig) -> None:
        assert 'rbln' in current_platform.get_device_name().lower()
        self.cache_config = cache_config
        self.model_config = model_config
        self.parallel_config = parallel_config
        self.head_size = model_config.get_head_size()
        self.num_layers = model_config.get_num_layers(parallel_config)
        if RBLNWorker.disable_tp and parallel_config.enable_expert_parallel:
            self.num_heads = model_config.get_total_num_kv_heads()
        else:
            self.num_heads = model_config.get_num_kv_heads(parallel_config)
        self.block_size = cache_config.block_size
        self.num_cpu_blocks = cache_config.num_gpu_blocks
        if cache_config.cache_dtype == 'auto':
            self.dtype = STR_DTYPE_TO_TORCH_DTYPE['float']
        else:
            self.dtype = STR_DTYPE_TO_TORCH_DTYPE[cache_config.cache_dtype]
        self.attn_backend = get_attn_backend(self.model_config.get_head_size(), self.model_config.dtype, cache_config.cache_dtype, self.block_size, self.model_config.is_attention_free)
        logger.info('[RBLN] initialize cache engine')
        self.cpu_cache = self._allocate_kv_cache()

    def _allocate_kv_cache(self) -> List[torch.Tensor]:
        """Allocates KV cache on RBLN."""
        kv_cache_shape = self.attn_backend.get_kv_cache_shape(self.num_cpu_blocks + 1, self.block_size, self.num_heads, self.head_size)
        kv_cache: List[torch.Tensor] = []
        logger.info('[RBLN] attention backend get_kv_cache_shape = %s', kv_cache_shape)
        logger.info('[RBLN] allocate kv cache shape = %s', kv_cache_shape)
        kv_cache_size = 1
        for dim in kv_cache_shape:
            kv_cache_size *= dim
        logger.info('[RBLN] 1 layer : allocate kv cache size = %d', kv_cache_size)
        kv_cache_size *= self.num_layers
        logger.info('[RBLN] all layers : allocate kv cache size = %d', kv_cache_size)
        for _ in range(self.num_layers):
            kv_cache.append(torch.empty(kv_cache_shape, dtype=self.dtype, device='cpu'))
        logger.info('[RBLN] allocate kv cache length = %d', len(kv_cache))
        return kv_cache

    def swap_in(self, src_to_dst: Dict[int, int]) -> None:
        raise NotImplementedError('Swap is not supported in RBLNCacheEngine.')

    def swap_out(self, src_to_dst: Dict[int, int]) -> None:
        raise NotImplementedError('Swap is not supported in RBLNCacheEngine.')

    def copy(self, src_to_dsts: Dict[int, List[int]]) -> None:
        logger.info('[RBLN] copy kv cache')
        self.attn_backend.copy_blocks(self.cpu_cache, src_to_dsts)

    @staticmethod
    def get_cache_block_size(block_size: int, cache_dtype: str, model_config: ModelConfig, parallel_config: ParallelConfig) -> int:
        head_size = model_config.get_head_size()
        if RBLNWorker.disable_tp and parallel_config.enable_expert_parallel:
            num_heads = model_config.get_total_num_kv_heads()
        else:
            num_heads = model_config.get_num_kv_heads(parallel_config)
        num_layers = model_config.get_num_layers(parallel_config)
        key_cache_block = block_size * num_heads * head_size
        value_cache_block = key_cache_block
        total = num_layers * (key_cache_block + value_cache_block)
        if cache_dtype == 'auto':
            dtype = STR_DTYPE_TO_TORCH_DTYPE['float']
        else:
            dtype = STR_DTYPE_TO_TORCH_DTYPE[cache_dtype]
        dtype_size = torch.tensor([], dtype=dtype).element_size()
        total_size = dtype_size * total
        logger.info('[RBLN] get kv cache block size = %d', total_size)
        return total_size