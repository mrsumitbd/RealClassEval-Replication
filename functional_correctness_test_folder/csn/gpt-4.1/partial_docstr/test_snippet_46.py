import pytest
import snippet_46 as module_0

def test_case_0():
    bytes_0 = b'\x9a\x96T\xe1\xee\xb0]cn\x97@\x88\xa0$|\xd4\xa4\x94\xdb\xff'
    share_class_0 = module_0.ShareClass()
    assert f'{type(share_class_0).__module__}.{type(share_class_0).__qualname__}' == 'snippet_46.ShareClass'
    with pytest.raises(NotImplementedError):
        share_class_0.canonical_uri(bytes_0)

def test_case_1():
    share_class_0 = module_0.ShareClass()
    assert f'{type(share_class_0).__module__}.{type(share_class_0).__qualname__}' == 'snippet_46.ShareClass'
    with pytest.raises(NotImplementedError):
        share_class_0.service_number()

def test_case_2():
    share_class_0 = module_0.ShareClass()
    assert f'{type(share_class_0).__module__}.{type(share_class_0).__qualname__}' == 'snippet_46.ShareClass'
    var_0 = share_class_0.magic()
    with pytest.raises(NotImplementedError):
        share_class_0.extract(var_0)

def test_case_3():
    float_0 = -434.91
    dict_0 = {}
    share_class_0 = module_0.ShareClass(**dict_0)
    assert f'{type(share_class_0).__module__}.{type(share_class_0).__qualname__}' == 'snippet_46.ShareClass'
    with pytest.raises(NotImplementedError):
        share_class_0.extract(float_0)