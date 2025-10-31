import snippet_161 as module_0

def test_case_0():
    none_type_0 = None
    s_r_t_cue_block_0 = module_0.SRTCueBlock(none_type_0, none_type_0, none_type_0, none_type_0)
    assert f'{type(s_r_t_cue_block_0).__module__}.{type(s_r_t_cue_block_0).__qualname__}' == 'snippet_161.SRTCueBlock'
    assert s_r_t_cue_block_0.index is None
    assert s_r_t_cue_block_0.start is None
    assert s_r_t_cue_block_0.end is None
    assert s_r_t_cue_block_0.payload is None
    assert f'{type(module_0.SRTCueBlock.CUE_TIMINGS_PATTERN).__module__}.{type(module_0.SRTCueBlock.CUE_TIMINGS_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.SRTCueBlock.is_valid).__module__}.{type(module_0.SRTCueBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.SRTCueBlock.from_lines).__module__}.{type(module_0.SRTCueBlock.from_lines).__qualname__}' == 'builtins.method'