import pytest
import snippet_52 as module_0

def test_case_0():
    bit_field_0 = module_0.BitField()
    assert f'{type(bit_field_0).__module__}.{type(bit_field_0).__qualname__}' == 'snippet_52.BitField'
    none_type_0 = None
    bit_field_0.__call__(none_type_0)
    bit_field_0.__call__(bit_field_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = False
    set_0 = {bool_0, bool_0, bool_0}
    bool_1 = False
    list_0 = [bool_1]
    bit_field_0 = module_0.BitField(*list_0)
    assert f'{type(bit_field_0).__module__}.{type(bit_field_0).__qualname__}' == 'snippet_52.BitField'
    bit_field_0.__call__(set_0)

def test_case_2():
    int_0 = 594
    list_0 = [int_0, int_0, int_0]
    bit_field_0 = module_0.BitField(*list_0)
    assert f'{type(bit_field_0).__module__}.{type(bit_field_0).__qualname__}' == 'snippet_52.BitField'
    bit_field_1 = module_0.BitField()
    assert f'{type(bit_field_1).__module__}.{type(bit_field_1).__qualname__}' == 'snippet_52.BitField'
    bit_field_1.__call__(list_0)
    var_0 = bit_field_0.__call__(int_0)
    assert var_0 == 594

def test_case_3():
    bit_field_0 = module_0.BitField()
    assert f'{type(bit_field_0).__module__}.{type(bit_field_0).__qualname__}' == 'snippet_52.BitField'
    int_0 = 2
    var_0 = bit_field_0.__call__(int_0)
    list_0 = [int_0, int_0, int_0, int_0, var_0, int_0, int_0, var_0]
    bit_field_1 = module_0.BitField(*list_0)
    assert f'{type(bit_field_1).__module__}.{type(bit_field_1).__qualname__}' == 'snippet_52.BitField'
    bit_field_0.__call__(var_0)
    var_1 = bit_field_1.__call__(int_0)
    assert var_1 == 2