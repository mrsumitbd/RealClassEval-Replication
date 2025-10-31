import pytest
import snippet_172 as module_0

def test_case_0():
    bytes_0 = b'c\xbbDQ\x8dv\x11\xd2\xea\xec[\xc8'
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(none_type_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things is None
    assert multiple_things_0.name is None
    multiple_things_0.get_thing(bytes_0)
    none_type_1 = None
    multiple_things_1 = module_0.MultipleThings(none_type_1, bytes_0)
    assert f'{type(multiple_things_1).__module__}.{type(multiple_things_1).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_1.things is None
    assert multiple_things_1.name == b'c\xbbDQ\x8dv\x11\xd2\xea\xec[\xc8'
    var_0 = multiple_things_1.get_name()
    assert var_0 == b'c\xbbDQ\x8dv\x11\xd2\xea\xec[\xc8'

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = -1785
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(int_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things == -1785
    assert multiple_things_0.name is None
    multiple_things_0.get_thing(none_type_0)

def test_case_2():
    float_0 = -98.093463
    bytes_0 = b'!(\x06N\xcd8\xb2\xfe|\xda\x1c'
    multiple_things_0 = module_0.MultipleThings(bytes_0, bytes_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things == b'!(\x06N\xcd8\xb2\xfe|\xda\x1c'
    assert multiple_things_0.name == b'!(\x06N\xcd8\xb2\xfe|\xda\x1c'
    var_0 = multiple_things_0.get_things()
    assert var_0 == b'!(\x06N\xcd8\xb2\xfe|\xda\x1c'
    multiple_things_0.get_thing(float_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    bool_0 = True
    bool_1 = False
    multiple_things_0 = module_0.MultipleThings(bool_1, bool_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things is False
    assert multiple_things_0.name is True
    multiple_things_0.get_thing(bool_1)

def test_case_4():
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(none_type_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things is None
    assert multiple_things_0.name is None

def test_case_5():
    complex_0 = 744.3 - 1246.313028j
    multiple_things_0 = module_0.MultipleThings(complex_0, complex_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things == 744.3 - 1246.313028j
    assert multiple_things_0.name == 744.3 - 1246.313028j
    var_0 = multiple_things_0.get_things()
    assert var_0 == 744.3 - 1246.313028j

def test_case_6():
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(none_type_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things is None
    assert multiple_things_0.name is None
    multiple_things_0.get_name()

@pytest.mark.xfail(strict=True)
def test_case_7():
    bool_0 = False
    bool_1 = False
    set_0 = {bool_1, bool_1}
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(set_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things == {False}
    assert multiple_things_0.name is None
    multiple_things_0.get_thing(bool_0)

def test_case_8():
    bool_0 = True
    set_0 = {bool_0, bool_0}
    none_type_0 = None
    multiple_things_0 = module_0.MultipleThings(set_0, none_type_0)
    assert f'{type(multiple_things_0).__module__}.{type(multiple_things_0).__qualname__}' == 'snippet_172.MultipleThings'
    assert multiple_things_0.things == {True}
    assert multiple_things_0.name is None
    multiple_things_0.get_thing(bool_0)