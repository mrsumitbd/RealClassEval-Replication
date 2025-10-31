import snippet_121 as module_0

def test_case_0():
    excels_0 = module_0.Excels()
    assert f'{type(module_0.Excels.read).__module__}.{type(module_0.Excels.read).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.Excels.read_opyxl).__module__}.{type(module_0.Excels.read_opyxl).__qualname__}' == 'builtins.method'
    assert f'{type(module_0.Excels.clean).__module__}.{type(module_0.Excels.clean).__qualname__}' == 'builtins.method'