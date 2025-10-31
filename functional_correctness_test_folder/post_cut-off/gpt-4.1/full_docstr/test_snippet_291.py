import pytest
import snippet_291 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    none_type_0 = None
    progress_scope_0 = module_0.ProgressScope(bool_0, bool_0, none_type_0)
    assert f'{type(progress_scope_0).__module__}.{type(progress_scope_0).__qualname__}' == 'snippet_291.ProgressScope'
    assert progress_scope_0.context is False
    assert progress_scope_0.total is False
    assert progress_scope_0.description is None
    assert progress_scope_0.current == 0
    progress_scope_0.update()

@pytest.mark.xfail(strict=True)
def test_case_1():
    int_0 = 3132
    none_type_0 = None
    progress_scope_0 = module_0.ProgressScope(none_type_0, int_0, none_type_0)
    assert f'{type(progress_scope_0).__module__}.{type(progress_scope_0).__qualname__}' == 'snippet_291.ProgressScope'
    assert progress_scope_0.context is None
    assert progress_scope_0.total == 3132
    assert progress_scope_0.description is None
    assert progress_scope_0.current == 0
    progress_scope_0.update()

def test_case_2():
    none_type_0 = None
    progress_scope_0 = module_0.ProgressScope(none_type_0, none_type_0, none_type_0)
    assert f'{type(progress_scope_0).__module__}.{type(progress_scope_0).__qualname__}' == 'snippet_291.ProgressScope'
    assert progress_scope_0.context is None
    assert progress_scope_0.total is None
    assert progress_scope_0.description is None
    assert progress_scope_0.current == 0

@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    float_0 = -1928.1454
    none_type_1 = None
    progress_scope_0 = module_0.ProgressScope(float_0, none_type_1, float_0)
    assert f'{type(progress_scope_0).__module__}.{type(progress_scope_0).__qualname__}' == 'snippet_291.ProgressScope'
    assert progress_scope_0.context == pytest.approx(-1928.1454, abs=0.01, rel=0.01)
    assert progress_scope_0.total is None
    assert progress_scope_0.description == pytest.approx(-1928.1454, abs=0.01, rel=0.01)
    assert progress_scope_0.current == 0
    progress_scope_0.set_progress(none_type_0)