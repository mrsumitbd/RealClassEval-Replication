from vllm.lora.worker_manager import LRUCacheWorkerLoRAManager
from vllm.lora.models import LoRAModel
from typing import List
from vllm.lora.utils import get_adapter_absolute_path

class VLLMHijack:

    @staticmethod
    def hijack():

        def hijack__load_adapter(self, lora_request: TensorLoRARequest) -> LoRAModel:
            """
            based on vllm.lora.worker_manager.WorkerLoRAManager._load_adapter, support load adapter with lora tensors

            Reason:
            VLLM does not support adding LoRA from tensors directly. It only supports adding LoRA via file paths.
            To synchronize the LoRA tensors of the actor model, we need to find a workaround to enable VLLM to load memory-based LoRA tensors.
            """
            try:
                supported_lora_modules = self._adapter_manager.supported_lora_modules
                packed_modules_mapping = self._adapter_manager.packed_modules_mapping
                expected_lora_modules: List[str] = []
                for module in supported_lora_modules:
                    if module in packed_modules_mapping:
                        expected_lora_modules.extend(packed_modules_mapping[module])
                    else:
                        expected_lora_modules.append(module)
                expected_lora_modules = list(set(expected_lora_modules))
                lora_tensors = None
                from vllm.lora.peft_helper import PEFTHelper
                if isinstance(lora_request, TensorLoRARequest):
                    peft_config = lora_request.peft_config
                    lora_tensors = lora_request.lora_tensors
                    peft_helper = PEFTHelper.from_dict(peft_config)
                else:
                    lora_path = get_adapter_absolute_path(lora_request.lora_path)
                    peft_helper = PEFTHelper.from_local_dir(lora_path, self.max_position_embeddings)
                peft_helper.validate_legal(self.lora_config)
                model = self._adapter_manager.model
                hf_to_vllm_mapper = None
                if hasattr(model, 'hf_to_vllm_mapper') and model.hf_to_vllm_mapper is not None:
                    hf_to_vllm_mapper = model.hf_to_vllm_mapper
                if isinstance(lora_request, TensorLoRARequest):
                    lora = self._lora_model_cls.from_lora_tensors(lora_model_id=lora_request.lora_int_id, tensors=lora_tensors, peft_helper=peft_helper, device='cpu', dtype=self.lora_config.lora_dtype, embeddings=None, target_embedding_padding=self.vocab_size + self.lora_config.lora_extra_vocab_size, embedding_modules=self.embedding_modules, embedding_padding_modules=self.embedding_padding_modules, weights_mapper=hf_to_vllm_mapper)
                else:
                    lora = self._lora_model_cls.from_local_checkpoint(lora_path, expected_lora_modules, peft_helper=peft_helper, lora_model_id=lora_request.lora_int_id, device='cpu', dtype=self.lora_config.lora_dtype, target_embedding_padding=self.vocab_size + self.lora_config.lora_extra_vocab_size, embedding_modules=self.embedding_modules, embedding_padding_modules=self.embedding_padding_modules, weights_mapper=hf_to_vllm_mapper)
            except Exception as e:
                raise e
            if lora.extra_vocab_size > self.lora_config.lora_extra_vocab_size:
                raise ValueError(f'LoRA added vocab size {lora.extra_vocab_size} is greater than lora_extra_vocab_size {self.lora_config.lora_extra_vocab_size}.')
            return lora

        def do_hijack(target_cls, target_method_name, hooking_method):
            setattr(target_cls, target_method_name, hooking_method)
        do_hijack(LRUCacheWorkerLoRAManager, '_load_adapter', hijack__load_adapter)