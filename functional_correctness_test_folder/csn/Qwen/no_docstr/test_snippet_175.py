import pytest
import snippet_175 as module_0

def test_case_0():
    s2_image_0 = module_0.S2Image()
    assert f'{type(s2_image_0).__module__}.{type(s2_image_0).__qualname__}' == 'snippet_175.S2Image'
    with pytest.raises(NotImplementedError):
        s2_image_0.extend(s2_image_0, s2_image_0, s2_image_0)

def test_case_1():
    s2_image_0 = module_0.S2Image()
    assert f'{type(s2_image_0).__module__}.{type(s2_image_0).__qualname__}' == 'snippet_175.S2Image'
    with pytest.raises(NotImplementedError):
        s2_image_0.usage()