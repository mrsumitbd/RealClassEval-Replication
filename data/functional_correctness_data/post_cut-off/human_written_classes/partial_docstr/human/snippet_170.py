from skyrl_train.distributed.utils import init_custom_process_group
import warnings
from torch.distributed import destroy_process_group
from skyrl_train.utils import str_to_torch_dtype
import torch
from typing import List, Any, Dict, Optional

class WorkerWrap:

    def test_rpc(self, *args, **kwargs):
        """Test RPC call to worker"""
        return (args, kwargs)

    def init_weight_update_communicator(self, master_address, master_port, rank_offset, world_size, group_name, backend='nccl', override_existing: bool=False):
        """Init torch process group for model weights update"""
        assert torch.distributed.is_initialized(), 'default torch process group must be initialized'
        assert group_name != '', 'group name must not be empty'
        if getattr(self, '_model_update_group', None):
            if override_existing:
                print('Destroying existing model update group')
                destroy_process_group(self._model_update_group)
                self._model_update_group = None
            else:
                warnings.warn('Detected an existing weights update group. For overriding, use `generator.override_existing_update_group=True`')
        rank = torch.distributed.get_rank() + rank_offset
        print(f'torch.distributed.get_rank(): {torch.distributed.get_rank()}, rank_offset: {rank_offset}, rank: {rank}, world_size: {world_size}, group_name: {group_name}')
        self._model_update_group = init_custom_process_group(backend=backend, init_method=f'tcp://{master_address}:{master_port}', world_size=world_size, rank=rank, group_name=group_name)
        print(f'init_weight_update_communicator: master_address={master_address}, master_port={master_port}, ', f'rank={rank}, world_size={world_size}, group_name={group_name}')

    def update_weights(self, names: List[str], dtypes: List[str], shapes: List[List[int]]):
        """Broadcast weight to all vllm workers from source rank 0 (actor model)"""
        weight_list = []
        for name, dtype, shape in zip(names, dtypes, shapes):
            dtype = str_to_torch_dtype(dtype)
            assert dtype == self.model_config.dtype, f'mismatch dtype: src {dtype}, dst {self.model_config.dtype}'
            weight = torch.empty(shape, dtype=dtype, device='cuda')
            torch.distributed.broadcast(weight, 0, group=self._model_update_group)
            weight_list.append((name, weight))
        self.model_runner.model.load_weights(weights=weight_list)
        for weight in weight_list:
            del weight

    def update_weights_cuda_ipc(self, names: List[str], dtypes: List[str], shapes: List[int], ipc_handles: List[Dict[str, Any]]):
        weight_list = []
        for name, dtype, shape, ipc_handle in zip(names, dtypes, shapes, ipc_handles):
            dtype = str_to_torch_dtype(dtype)
            device = torch.cuda.current_device()
            props = torch.cuda.get_device_properties(device)
            physical_gpu_id = str(props.uuid)
            assert dtype == self.model_config.dtype, f'mismatch dtype: src {dtype}, dst {self.model_config.dtype}'
            handle = ipc_handle[physical_gpu_id]
            device_id = self.device.index
            func, args = handle
            list_args = list(args)
            list_args[6] = device_id
            weight = func(*list_args)
            weight_list.append((name, weight))
        self.model_runner.model.load_weights(weights=weight_list)
        for weight in weight_list:
            del weight

    def destroy_weights_update_group(self):
        if not self._model_update_group:
            warnings.warn('No model update group to destroy')
            return
        destroy_process_group(self._model_update_group)