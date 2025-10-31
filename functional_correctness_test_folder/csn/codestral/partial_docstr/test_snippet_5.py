import pytest
import cookiecutter.exceptions as module_0
import snippet_5 as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    unknown_extension_0 = module_0.UnknownExtension()
    assert f'{type(unknown_extension_0).__module__}.{type(unknown_extension_0).__qualname__}' == 'cookiecutter.exceptions.UnknownExtension'
    tuple_0 = (unknown_extension_0,)
    dict_0 = {}
    module_1.ExtensionLoaderMixin(context=tuple_0, **dict_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    module_1.ExtensionLoaderMixin()