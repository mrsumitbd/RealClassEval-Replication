import pytest
import snippet_185 as module_0

def test_case_0():
    transport_0 = module_0.Transport()
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_185.Transport'
    assert f'{type(transport_0.options).__module__}.{type(transport_0.options).__qualname__}' == 'suds.transport.options.Options'

def test_case_1():
    transport_0 = module_0.Transport()
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_185.Transport'
    assert f'{type(transport_0.options).__module__}.{type(transport_0.options).__qualname__}' == 'suds.transport.options.Options'
    none_type_0 = None
    with pytest.raises(Exception):
        transport_0.open(none_type_0)

def test_case_2():
    float_0 = 633.0
    transport_0 = module_0.Transport()
    assert f'{type(transport_0).__module__}.{type(transport_0).__qualname__}' == 'snippet_185.Transport'
    assert f'{type(transport_0.options).__module__}.{type(transport_0.options).__qualname__}' == 'suds.transport.options.Options'
    with pytest.raises(Exception):
        transport_0.send(float_0)