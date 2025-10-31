import pytest
import snippet_187 as module_0

def test_case_0():
    float_0 = 1953.566
    node_finder_0 = module_0.NodeFinder(float_0, float_0)
    assert f'{type(node_finder_0).__module__}.{type(node_finder_0).__qualname__}' == 'snippet_187.NodeFinder'
    assert node_finder_0.matcher == pytest.approx(1953.566, abs=0.01, rel=0.01)
    assert node_finder_0.limit == pytest.approx(1953.566, abs=0.01, rel=0.01)