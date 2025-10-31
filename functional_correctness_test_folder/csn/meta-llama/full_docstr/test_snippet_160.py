import snippet_160 as module_0

def test_case_0():
    str_0 = "U'\x0c_i*$v/nEjKI'"
    s_b_v_cue_block_0 = module_0.SBVCueBlock(str_0, str_0, str_0)
    assert f'{type(s_b_v_cue_block_0).__module__}.{type(s_b_v_cue_block_0).__qualname__}' == 'snippet_160.SBVCueBlock'
    assert s_b_v_cue_block_0.start == "U'\x0c_i*$v/nEjKI'"
    assert s_b_v_cue_block_0.end == "U'\x0c_i*$v/nEjKI'"
    assert s_b_v_cue_block_0.payload == "U'\x0c_i*$v/nEjKI'"
    assert f'{type(module_0.SBVCueBlock.CUE_TIMINGS_PATTERN).__module__}.{type(module_0.SBVCueBlock.CUE_TIMINGS_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.SBVCueBlock.is_valid).__module__}.{type(module_0.SBVCueBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.SBVCueBlock.from_lines).__module__}.{type(module_0.SBVCueBlock.from_lines).__qualname__}' == 'builtins.method'