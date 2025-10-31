import snippet_163 as module_0

def test_case_0():
    str_0 = 'c4kW-8L-&\r|zND+/'
    web_v_t_t_style_block_0 = module_0.WebVTTStyleBlock(str_0)
    assert f'{type(web_v_t_t_style_block_0).__module__}.{type(web_v_t_t_style_block_0).__qualname__}' == 'snippet_163.WebVTTStyleBlock'
    assert web_v_t_t_style_block_0.text == 'c4kW-8L-&\r|zND+/'
    assert f'{type(module_0.WebVTTStyleBlock.STYLE_PATTERN).__module__}.{type(module_0.WebVTTStyleBlock.STYLE_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.WebVTTStyleBlock.is_valid).__module__}.{type(module_0.WebVTTStyleBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.WebVTTStyleBlock.from_lines).__module__}.{type(module_0.WebVTTStyleBlock.from_lines).__qualname__}' == 'builtins.method'

def test_case_1():
    str_0 = '\ts\tYrWzE}Tw.d:F\n!p+Q'
    web_v_t_t_style_block_0 = module_0.WebVTTStyleBlock(str_0)
    assert f'{type(web_v_t_t_style_block_0).__module__}.{type(web_v_t_t_style_block_0).__qualname__}' == 'snippet_163.WebVTTStyleBlock'
    assert web_v_t_t_style_block_0.text == '\ts\tYrWzE}Tw.d:F\n!p+Q'
    assert f'{type(module_0.WebVTTStyleBlock.STYLE_PATTERN).__module__}.{type(module_0.WebVTTStyleBlock.STYLE_PATTERN).__qualname__}' == 're.Pattern'
    assert f'{type(module_0.WebVTTStyleBlock.is_valid).__module__}.{type(module_0.WebVTTStyleBlock.is_valid).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.WebVTTStyleBlock.from_lines).__module__}.{type(module_0.WebVTTStyleBlock.from_lines).__qualname__}' == 'builtins.method'
    str_1 = "X8'}Zgv;)"
    str_2 = 'KT&sK2u;p'
    str_3 = 'U*yP_5d6y\n}]dj{'
    list_0 = [str_1, str_2, str_3, str_0]
    web_v_t_t_style_block_0.format_lines(list_0)