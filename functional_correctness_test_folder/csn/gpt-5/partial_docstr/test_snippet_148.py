import pytest
import snippet_148 as module_0
import txtorcon.util as module_1

def test_case_0():
    bool_0 = False
    addr_0 = module_0.Addr(bool_0)
    assert f'{type(addr_0).__module__}.{type(addr_0).__qualname__}' == 'snippet_148.Addr'
    assert addr_0.map is False
    assert addr_0.ip is None
    assert addr_0.name is None
    assert addr_0.expiry is None
    assert addr_0.expires is None
    assert addr_0.created is None

@pytest.mark.xfail(strict=True)
def test_case_1():
    float_0 = 358.25
    addr_0 = module_0.Addr(float_0)
    assert f'{type(addr_0).__module__}.{type(addr_0).__qualname__}' == 'snippet_148.Addr'
    assert addr_0.map == pytest.approx(358.25, abs=0.01, rel=0.01)
    assert addr_0.ip is None
    assert addr_0.name is None
    assert addr_0.expiry is None
    assert addr_0.expires is None
    assert addr_0.created is None
    var_0 = module_1.maybe_ip_addr(addr_0)
    assert module_1.GeoIP is None
    assert module_1.city is None
    assert module_1.country is None
    assert module_1.asn is None
    assert module_1.CRYPTOVARIABLE_EQUALITY_COMPARISON_NONCE == b'\x97\xe2\xb6v\x9d\xd0\x10\xd3\x82\x10\x8c\xe6L\xfe&\x9a$\x90\x8b@\x82+=\xfcwR9\xe0R\xc5\x81\x8b'
    list_0 = [var_0, float_0, addr_0, var_0]
    addr_0.update(*list_0)

@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    addr_0 = module_0.Addr(none_type_0)
    assert f'{type(addr_0).__module__}.{type(addr_0).__qualname__}' == 'snippet_148.Addr'
    assert addr_0.map is None
    assert addr_0.ip is None
    assert addr_0.name is None
    assert addr_0.expiry is None
    assert addr_0.expires is None
    assert addr_0.created is None
    var_0 = module_1.maybe_ip_addr(none_type_0)
    assert var_0 == 'None'
    assert module_1.GeoIP is None
    assert module_1.city is None
    assert module_1.country is None
    assert module_1.asn is None
    assert module_1.CRYPTOVARIABLE_EQUALITY_COMPARISON_NONCE == b'\x97\xe2\xb6v\x9d\xd0\x10\xd3\x82\x10\x8c\xe6L\xfe&\x9a$\x90\x8b@\x82+=\xfcwR9\xe0R\xc5\x81\x8b'
    addr_0.update(*var_0)

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    addr_0 = module_0.Addr(none_type_0)
    assert f'{type(addr_0).__module__}.{type(addr_0).__qualname__}' == 'snippet_148.Addr'
    assert addr_0.map is None
    assert addr_0.ip is None
    assert addr_0.name is None
    assert addr_0.expiry is None
    assert addr_0.expires is None
    assert addr_0.created is None
    var_0 = module_1.maybe_ip_addr(none_type_0)
    assert var_0 == 'None'
    assert module_1.GeoIP is None
    assert module_1.city is None
    assert module_1.country is None
    assert module_1.asn is None
    assert module_1.CRYPTOVARIABLE_EQUALITY_COMPARISON_NONCE == b'\x97\xe2\xb6v\x9d\xd0\x10\xd3\x82\x10\x8c\xe6L\xfe&\x9a$\x90\x8b@\x82+=\xfcwR9\xe0R\xc5\x81\x8b'
    tuple_0 = (var_0, var_0, var_0)
    addr_0.update(*tuple_0)