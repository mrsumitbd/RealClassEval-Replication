import pytest
import builtins as module_0
import snippet_237 as module_1

@pytest.mark.xfail(strict=True)
def test_case_0():
    exception_0 = module_0.Exception()
    module_1.TreeDecorator(exception_0, exception_0, exception_0)

@pytest.mark.xfail(strict=True)
def test_case_1():
    none_type_0 = None
    module_1.TreeDecorator(none_type_0, none_type_0, none_type_0)