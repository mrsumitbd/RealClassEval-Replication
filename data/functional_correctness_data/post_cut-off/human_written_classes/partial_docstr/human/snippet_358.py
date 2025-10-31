from typing import Dict, List, Optional

class MegatronMemoryBufferForRollout:
    """
    We assume that
    - inference engine has tp + dp
    - actor has tp + pp + dp
    - the tp between inference engine and actor should be the same
    - memory_buffers: contains a list of memory_buffers, each is a dict from dtype to MemoryBuffer
    - weight_buffers: contains a list of weight_buffers, each is a dict from name to param
    - named_parameters: a dict from name to parameter that normalizes the names from pp and vpp. Note that
        the named_parameters may not be directly compatible with inference engine. User has to take care of
        this part such as the layout mismatches. (e.g. qkv transpose)
    - Note that weight_buffer, named_parameters and memory_buffers share the same underlying GPU memory.
    - When doing weight sync, the data is transfer via memory buffers
    """

    def __init__(self, transform_memory_param_fn):
        self._memory_buffers = []
        self._weight_buffers = []
        self._named_parameters = {}
        self.transform_memory_param_fn = transform_memory_param_fn

    def initialize_weight_buffer(self, weight_buffer_meta_pp: List[Dict[str, Dict]]):
        """
        Initialize the weight buffer. The weight buffer is obtained according to the actor. We will construct
        a large buffer for each dtype in the weight_buffer.

        Args:
            weight_buffer_meta: contains pp models, each pp models contains a dictionary of mapping from

        Returns: None

        """
        self.weight_buffer_meta_pp = weight_buffer_meta_pp
        for weight_buffer_meta in self.weight_buffer_meta_pp:
            memory_buffer = build_memory_buffer(weight_buffer_meta)
            self._memory_buffers.append(memory_buffer)
            self._weight_buffers.append(None)

    def build_memory_reference(self):
        for i, weight_buffer_meta in enumerate(self.weight_buffer_meta_pp):
            self._weight_buffers[i] = build_memory_reference(weight_buffer_meta, self._memory_buffers[i])
        self._named_parameters = self.transform_memory_param_fn(self._weight_buffers)

    @property
    def named_parameters(self):
        return self._named_parameters

    @property
    def weight_buffers(self):
        return self._weight_buffers

    @property
    def memory_buffers(self):
        return self._memory_buffers