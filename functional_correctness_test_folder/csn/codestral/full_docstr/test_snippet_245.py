import pytest
import snippet_245 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    sampleable_0 = module_0.Sampleable()
    assert f'{type(sampleable_0).__module__}.{type(sampleable_0).__qualname__}' == 'snippet_245.Sampleable'
    assert sampleable_0.sample is None
    sampleable_0.get_sample()