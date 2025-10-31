from cosmos_rl.policy.model.base import WeightMapper
from typing import Dict, List, Tuple, Callable, Any, Optional, Union
from cosmos_rl.utils.logging import logger
from cosmos_rl.utils.parallelism import ParallelDims
from cosmos_rl.utils.constant import COSMOS_HF_MODEL_TYPES

class ParallelTopoMapperGroup:
    """
    A class to represent a group of weight sharing topology maps used for weight synchronization.
    This class manages multiple ParallelTopoMapper instances, each corresponding to a different parallelism strategy.
    Different model parts may have different parallelism strategies in one whole model.
    It is used to prepare local shard information for parameters based on the parallelism configuration.
    It clusters parameters by model part and prepares local shard information for each part.
    """

    def __init__(self, global_parallelism: ParallelDims, hf_config: Any, is_policy: bool, underlying_model: Any, backend: str='vllm', weight_mapper: Optional[WeightMapper]=None):
        """
        Initialize the ParallelTopoMapperGroup with the given parallelism configurations.

        :param global_parallelism: The parallelism config for the policy or rollout.
        :param hf_config: The huggingface config.
        :param is_policy: A boolean indicating if this is for policy parallelism.
        :param underlying_model: The underlying model for which the parallelism map is created.
        :param weight_mapper: An optional WeightMapper instance. If None, a default mapper is used based on the model type from hf_config.
        """
        self.hf_config = hf_config
        model_type = hf_config.model_type
        self.mapper_group: List[ParallelTopoMapper] = []
        self.backend = backend
        if weight_mapper is None:
            if model_type not in WeightMapper._MODEL_WEIGHT_MAPPER_REGISTRY:
                logger.warning(f'[ParallelTopoMapperGroup] can not find {model_type} in weight mapper, use {COSMOS_HF_MODEL_TYPES} model type instead.')
                model_type = COSMOS_HF_MODEL_TYPES
            weight_mapper_fn = WeightMapper.get_weight_mapper(model_type)
            self.weight_mapper = weight_mapper_fn(hf_config)
        else:
            self.weight_mapper = weight_mapper
        if is_policy:
            strategies = self.weight_mapper.get_policy_parallelism_strategy()
        else:
            strategies = self.weight_mapper.get_rollout_parallelism_strategy()
        if strategies:
            for strategy in strategies:
                self.mapper_group.append(ParallelTopoMapper(global_parallelism, strategy, weight_mapper, hf_config, is_policy=is_policy, backend=self.backend, underlying_model=underlying_model))
        else:
            self.mapper_group.append(ParallelTopoMapper(global_parallelism, None, weight_mapper, hf_config, is_policy=is_policy, backend=self.backend, underlying_model=underlying_model))

    def _cluster_params_by_model_part(self, params: List[Tuple[str, int]]) -> List[List[Tuple[str, int]]]:
        """
        Resort the parameters based on the name mapper.
        :param params: The parameters to resort.
        :return: A list of tuples containing the resorted parameters separated by different model parts.
        """
        if len(self.mapper_group) == 1:
            return [params]
        x = [[] for _ in self.mapper_group]
        for name, rank in params:
            idx = self.weight_mapper.name_to_model_part_index(name)
            x[idx].append((name, rank))
        return x

    def prepare_local_shard_infos(self, hf_key_n_rank: List[Tuple[str, int]], global_rank: int) -> Dict[str, Any]:
        """
        Prepare local shard information for the given parameters based on the parallelism configuration.
        :param hf_key_n_rank: A list of tuples containing the parameter names and their shape ranks.
        :param global_rank: The global rank to prepare local shard information for.
        :return: A dictionary containing the local shard information for each parameter of that rank.
        """
        x = self._cluster_params_by_model_part(hf_key_n_rank)
        insts = {}
        for model_index, p in enumerate(x):
            insts.update(self.mapper_group[model_index].local_shard_info_for_params(p, global_rank))
        return insts