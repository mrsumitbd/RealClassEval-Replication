from typing import TYPE_CHECKING, List, Tuple

class FlopsCounter:
    """
    Used to count mfu during training loop

    Example:
        flops_counter = FlopsCounter(config)
        flops_achieved, flops_promised = flops_counter.estimate_flops(tokens_list, delta_time)
    """

    def __init__(self, config: 'LlamaConfig'):
        _ESTIMATE_FUNC = {'llama': self._estimate_llama_flops, 'qwen2': self._estimate_llama_flops, 'qwen2_vl': self._estimate_llama_flops, 'qwen2_5_vl': self._estimate_llama_flops, 'qwen3': self._estimate_llama_flops}
        if config.model_type not in _ESTIMATE_FUNC:
            print(f'Only support {_ESTIMATE_FUNC.keys()}, but got {config.model_type}. MFU will always be zero.')
        self.config = config
        self._estimate_flops = _ESTIMATE_FUNC.get(config.model_type, self._estimate_unknown_flops)

    def _estimate_unknown_flops(self, tokens_sum: int, batch_seqlens: List[int], delta_time: float) -> float:
        return 0

    def _estimate_llama_flops(self, tokens_sum: int, batch_seqlens: List[int], delta_time: float) -> float:
        hidden_size = self.config.hidden_size
        vocab_size = self.config.vocab_size
        num_hidden_layers = self.config.num_hidden_layers
        num_key_value_heads = self.config.num_key_value_heads
        num_attention_heads = self.config.num_attention_heads
        intermediate_size = self.config.intermediate_size
        head_dim = hidden_size // num_attention_heads
        q_size = num_attention_heads * head_dim
        k_size = num_key_value_heads * head_dim
        v_size = num_key_value_heads * head_dim
        mlp_N = hidden_size * intermediate_size * 3
        attn_linear_N = hidden_size * (q_size + k_size + v_size + num_attention_heads * head_dim)
        emd_and_lm_head_N = vocab_size * hidden_size * 2
        dense_N = (mlp_N + attn_linear_N) * num_hidden_layers + emd_and_lm_head_N
        dense_N_flops = 6 * dense_N * tokens_sum
        seqlen_square_sum = 0
        for seqlen in batch_seqlens:
            seqlen_square_sum += seqlen * seqlen
        attn_qkv_flops = 12 * seqlen_square_sum * head_dim * num_attention_heads * num_hidden_layers
        flops_all_token = dense_N_flops + attn_qkv_flops
        flops_achieved = flops_all_token * (1.0 / delta_time) / 1000000000000.0
        return flops_achieved

    def estimate_flops(self, batch_seqlens: List[int], delta_time: float) -> Tuple[float, float]:
        """
        Estimate the FLOPS based on the number of valid tokens in the current batch and the time taken.

        Args:
            batch_seqlens (List[int]): A list where each element represents the number of valid tokens in the current batch.
            delta_time (float): The time taken to process the batch, in seconds.

        Returns:
            estimated_flops (float): The estimated FLOPS based on the input tokens and time.
            promised_flops (float): The expected FLOPS of the current device.
        """
        tokens_sum = sum(batch_seqlens)
        estimated_flops = self._estimate_flops(tokens_sum, batch_seqlens, delta_time)
        promised_flops = get_device_flops()
        return (estimated_flops, promised_flops)