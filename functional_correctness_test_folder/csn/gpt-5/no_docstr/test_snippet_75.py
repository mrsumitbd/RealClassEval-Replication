import pytest
import snippet_75 as module_0

def test_case_0():
    geometry_0 = module_0.Geometry()
    assert f'{type(geometry_0).__module__}.{type(geometry_0).__qualname__}' == 'snippet_75.Geometry'
    with pytest.raises(NotImplementedError):
        geometry_0.geojson()

def test_case_1():
    geometry_0 = module_0.Geometry()
    assert f'{type(geometry_0).__module__}.{type(geometry_0).__qualname__}' == 'snippet_75.Geometry'
    with pytest.raises(NotImplementedError):
        geometry_0.to_dict()