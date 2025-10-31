import pytest
import snippet_50 as module_0

def test_case_0():
    none_type_0 = None
    met_py_checker_0 = module_0.MetPyChecker(none_type_0)
    assert f'{type(met_py_checker_0).__module__}.{type(met_py_checker_0).__qualname__}' == 'snippet_50.MetPyChecker'
    assert met_py_checker_0.tree is None
    assert module_0.MetPyChecker.name == 'snippet_50'
    assert module_0.MetPyChecker.version == '1.0'

@pytest.mark.xfail(strict=True)
def test_case_1():
    float_0 = -2392.6193
    none_type_0 = None
    met_py_checker_0 = module_0.MetPyChecker(none_type_0)
    assert f'{type(met_py_checker_0).__module__}.{type(met_py_checker_0).__qualname__}' == 'snippet_50.MetPyChecker'
    assert met_py_checker_0.tree is None
    assert module_0.MetPyChecker.name == 'snippet_50'
    assert module_0.MetPyChecker.version == '1.0'
    met_py_checker_0.error(float_0)