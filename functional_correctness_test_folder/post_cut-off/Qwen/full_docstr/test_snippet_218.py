import pytest
import snippet_218 as module_0

def test_case_0():
    str_0 = '{'
    c_block_0 = module_0.CBlock(str_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'

def test_case_1():
    none_type_0 = None
    c_block_0 = module_0.CBlock(none_type_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'

def test_case_2():
    str_0 = 'ga{nab<\\]LW`vb'
    c_block_0 = module_0.CBlock(str_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'
    var_0 = c_block_0.__str__()
    assert var_0 == 'ga{nab<\\]LW`vb'

def test_case_3():
    none_type_0 = None
    c_block_0 = module_0.CBlock(none_type_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'
    var_0 = c_block_0.__str__()
    assert var_0 == ''

def test_case_4():
    none_type_0 = None
    c_block_0 = module_0.CBlock(none_type_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'
    var_0 = c_block_0.__repr__()
    assert var_0 == 'CBlock(None, {})'

def test_case_5():
    bool_0 = True
    with pytest.raises(TypeError):
        module_0.CBlock(bool_0)

def test_case_6():
    str_0 = '(o\ttk['
    str_1 = ']@i_1eEmY>'
    str_2 = '\t\t^\rX'
    dict_0 = {str_0: str_0, str_1: str_0, str_2: str_1}
    c_block_0 = module_0.CBlock(str_0, dict_0)
    assert f'{type(c_block_0).__module__}.{type(c_block_0).__qualname__}' == 'snippet_218.CBlock'
    assert f'{type(module_0.CBlock.value).__module__}.{type(module_0.CBlock.value).__qualname__}' == 'builtins.property'
    var_0 = c_block_0.__repr__()
    assert var_0 == "CBlock((o\ttk[, {'(o\\ttk[': '(o\\ttk[', ']@i_1eEmY>': '(o\\ttk[', '\\t\\t^\\rX': ']@i_1eEmY>'})"
    float_0 = -1544.224
    none_type_0 = None
    c_block_1 = module_0.CBlock(none_type_0, none_type_0)
    assert f'{type(c_block_1).__module__}.{type(c_block_1).__qualname__}' == 'snippet_218.CBlock'
    with pytest.raises(TypeError):
        module_0.CBlock(float_0, c_block_1)