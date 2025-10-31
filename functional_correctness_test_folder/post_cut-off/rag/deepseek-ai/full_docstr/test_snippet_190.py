import pytest
import snippet_190 as module_0

@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    class_with_init_args_0 = module_0.ClassWithInitArgs(bool_0)
    assert f'{type(class_with_init_args_0).__module__}.{type(class_with_init_args_0).__qualname__}' == 'snippet_190.ClassWithInitArgs'
    assert class_with_init_args_0.cls is False
    assert class_with_init_args_0.args == ()
    assert class_with_init_args_0.kwargs == {}
    assert class_with_init_args_0.fused_worker_used is False
    class_with_init_args_0.__call__()