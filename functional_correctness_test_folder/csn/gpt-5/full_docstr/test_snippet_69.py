import snippet_69 as module_0

def test_case_0():
    bool_0 = False
    none_type_0 = None
    base_storage_0 = module_0.BaseStorage()
    assert f'{type(base_storage_0).__module__}.{type(base_storage_0).__qualname__}' == 'snippet_69.BaseStorage'
    base_storage_0.write(bool_0, none_type_0)

def test_case_1():
    float_0 = 282.6
    base_storage_0 = module_0.BaseStorage()
    assert f'{type(base_storage_0).__module__}.{type(base_storage_0).__qualname__}' == 'snippet_69.BaseStorage'
    var_0 = base_storage_0.exists(float_0)
    assert var_0 is False

def test_case_2():
    base_storage_0 = module_0.BaseStorage()
    assert f'{type(base_storage_0).__module__}.{type(base_storage_0).__qualname__}' == 'snippet_69.BaseStorage'
    var_0 = base_storage_0.max_file_idx()
    assert var_0 == 0
    var_1 = base_storage_0.exists(base_storage_0)
    assert var_1 is False