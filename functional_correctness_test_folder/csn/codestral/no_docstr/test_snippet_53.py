import snippet_53 as module_0

def test_case_0():
    int_0 = 1409
    bits_0 = module_0.Bits(int_0)
    assert f'{type(bits_0).__module__}.{type(bits_0).__qualname__}' == 'snippet_53.Bits'
    bits_0.__call__(int_0)

def test_case_1():
    none_type_0 = None
    bool_0 = False
    bits_0 = module_0.Bits(bool_0)
    assert f'{type(bits_0).__module__}.{type(bits_0).__qualname__}' == 'snippet_53.Bits'
    bits_0.__call__(none_type_0)

def test_case_2():
    bool_0 = True
    bits_0 = module_0.Bits(bool_0)
    assert f'{type(bits_0).__module__}.{type(bits_0).__qualname__}' == 'snippet_53.Bits'