import pytest
import snippet_272 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    user_context_form_view_mixin_0 = module_0.UserContextFormViewMixin()
    assert f'{type(user_context_form_view_mixin_0).__module__}.{type(user_context_form_view_mixin_0).__qualname__}' == 'snippet_272.UserContextFormViewMixin'
    user_context_form_view_mixin_0.get_agnocomplete_context()

@pytest.mark.xfail(strict=True)
def test_case_1():
    user_context_form_view_mixin_0 = module_0.UserContextFormViewMixin()
    assert f'{type(user_context_form_view_mixin_0).__module__}.{type(user_context_form_view_mixin_0).__qualname__}' == 'snippet_272.UserContextFormViewMixin'
    user_context_form_view_mixin_0.get_form_kwargs()