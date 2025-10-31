import pytest
import snippet_313 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    content_mixin_0 = module_0.ContentMixin()
    assert f'{type(content_mixin_0).__module__}.{type(content_mixin_0).__qualname__}' == 'snippet_313.ContentMixin'
    content_mixin_0.list_available_worlds()

@pytest.mark.xfail(strict=True)
def test_case_1():
    content_mixin_0 = module_0.ContentMixin()
    assert f'{type(content_mixin_0).__module__}.{type(content_mixin_0).__qualname__}' == 'snippet_313.ContentMixin'
    content_mixin_0.list_available_addons()